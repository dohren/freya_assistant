from pathlib import Path
from openai import OpenAI
import playsound
import re
import threading
import queue
import uuid

class OpenaiTTS:
    def __init__(self, speech_file_path="../resources/"):
        self.client = OpenAI()
        self.speech_file_path = Path(__file__).parent / speech_file_path
        self.audio_queue = queue.Queue()

    def speak(self, text):
        # Split text by sentences (considering periods and commas)
        sentences = re.split(r'(?<=[.?])\s*', text)
        
        # Start a thread to download and queue audio files
        download_thread = threading.Thread(target=self.download_audio_files, args=(sentences,))
        download_thread.start()
        
        # Play audio files as they are downloaded
        self.play_audio_files()
        
        # Wait for the download thread to finish
        download_thread.join()

    def download_audio_files(self, sentences):
        for sentence in sentences:
            if sentence:  # Skip any empty sentences
                response = self.client.audio.speech.create(
                    model="tts-1",
                    voice="nova",
                    input=sentence
                )

                # Save each sentence as a temporary file with a unique ID
                unique_id = uuid.uuid4()
                temp_file_path = self.speech_file_path / f"temp_{unique_id}.mp3"
                response.stream_to_file(temp_file_path)
                self.audio_queue.put(temp_file_path)
        
        # Signal that all files have been queued
        self.audio_queue.put(None)

    def play_audio_files(self):
        while True:
            temp_file_path = self.audio_queue.get()
            if temp_file_path is None:
                break  # Exit loop if the end signal is received
            playsound.playsound(str(temp_file_path), True)
            temp_file_path.unlink()  # Remove the temporary file after playing

if __name__ == "__main__":
    tts = OpenaiTTS()
    tts.speak("Guten Tag, wie geht es dir?")
    tts.speak("Frankreich ist ein Land in Westeuropa, bekannt für seine vielfältige Kultur, historischen Sehenswürdigkeiten und die französische Küche. Es ist das meistbesuchte Land der Welt, mit Attraktionen wie dem Eiffelturm in Paris, der Côte d'Azur und dem Schloss Versailles. Frankreich hat auch einen großen Einfluss auf die Kunst, Mode und Literatur weltweit. Guten Tag, wie geht es dir?")
