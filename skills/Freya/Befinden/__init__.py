import time
from openai_tts import OpenaiTTS
tts = OpenaiTTS()

def execute_skill(action, values):
    tts.speak("Mir geht es hervoragend. Und dir?")
