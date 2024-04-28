import sys
from common import OpenaiTTS

def execute_skill(action, values):
    tts = OpenaiTTS()
    tts.speak(values["text"])