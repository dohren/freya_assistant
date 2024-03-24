from pathlib import Path
from openai import OpenAI
import playsound

class OpenaiTTS:
    def __init__(self, speech_file_path="resources/speech.mp3"):
        self.client = OpenAI()
        self.speech_file_path = Path(__file__).parent / speech_file_path

    def synthesize_speech(self, text):
        response = self.client.audio.speech.create(
          model="tts-1",
          voice="nova",
          input=text
        )

        response.stream_to_file(self.speech_file_path)
        playsound.playsound(str(self.speech_file_path), True)

if __name__ == "__main__":
    tts = OpenaiTTS()
    tts.synthesize_speech("Guten Tag, wie geht es dir?")