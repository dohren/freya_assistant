import time
from openai_tts import OpenaiTTS


def execute_skill(action, values):
    tts = OpenaiTTS()
    tts.speak("Mir geht es hervoragend. Und dir?")
