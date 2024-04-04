
from datetime import datetime
from openai_tts import OpenaiTTS

def execute_skill(action, values):
    tts = OpenaiTTS()
    now = datetime.now()
    current_hour = now.strftime("%H")
    current_minute = now.strftime("%M")
    tts.speak(f"Es ist {current_hour} Uhr und {current_minute} Minuten.")