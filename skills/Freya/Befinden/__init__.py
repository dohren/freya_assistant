import time
from common import OpenaiTTS


def execute_skill(action, values):
    tts = OpenaiTTS()
    tts.speak("Mir geht es hervoragend. Und dir?")
