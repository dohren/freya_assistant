import pvporcupine
from pvrecorder import PvRecorder
import os
import struct
import pyaudio
import threading

class WakewordDetection(threading.Thread):
        
    
    def __init__(self, keywords, keyword_paths, model_path):
        threading.Thread.__init__(self)
        self.wake_word_detected = threading.Event()
        self.keywords = keywords
        self.access_key = os.getenv("PORCUPINE_ACCESS_KEY")
        self.keyword_paths = keyword_paths
        self.model_path = model_path

        self.porcupine = pvporcupine.create(access_key=self.access_key, keyword_paths=self.keyword_paths, model_path=self.model_path)
        
        self.sound = pyaudio.PyAudio()

        self.audio_stream = self.sound.open(
                    rate=self.porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=self.porcupine.frame_length)
        self.should_run = True

    def run(self):
        while self.should_run:
            pcm = self.audio_stream.read(self.porcupine.frame_length)
            pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

            keyword_index = self.porcupine.process(pcm)
            if keyword_index >= 0:
                print(f"Detected {self.keywords[keyword_index]}")
                self.wake_word_detected.set() 

        self.cleanup()

    def stop(self):
        self.should_run = False
        self.wake_word_detected.clear()  

    def cleanup(self):
        self.porcupine.delete()
        self.audio_stream.close()
        self.sound.terminate()

if __name__ == "__main__":
    keywords = ["hey freya"]
    keyword_paths = ['resources/freya.ppn']
    model_path = 'resources/porcupine_params_de.pv'

    wakeword_detection = WakewordDetection(keywords, keyword_paths, model_path)
    wakeword_detection.start()
    wakeword_detection.wake_word_detected.wait()  # Block until wake word is detected
    print("Wake word detected!")
    wakeword_detection.stop()
