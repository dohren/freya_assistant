import sys
from openai_tts import OpenaiTTS


def execute_skill(action, values):
    tts = OpenaiTTS()
    tts.speak("Tchüüss und Gute Nacht")
    sys.exit()