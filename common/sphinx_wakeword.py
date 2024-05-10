import time
import threading
from pocketsphinx import LiveSpeech

class WakewordDetection(threading.Thread):
        
    def __init__(self):
        threading.Thread.__init__(self)
        self.wake_word_detected = threading.Event()
        self.recognizer = LiveSpeech(kws='resources/wakewords.txt')

    def run(self):
        for phrase in self.recognizer:
            self.wake_word_detected.set()
            print(f"Detected {phrase}")

if __name__ == "__main__":
    wakeword_detection = WakewordDetection()
    wakeword_detection.start()
    wakeword_detection.wake_word_detected.wait()  # Block until wake word is detected
    print("Wake word detected!")
    wakeword_detection.join()
    


