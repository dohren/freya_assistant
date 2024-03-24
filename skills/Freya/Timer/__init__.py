import time
from openai_tts import OpenaiTTS


def sleep(duration):
    openai_tts = OpenaiTTS()
    openai_tts.synthesize_speech("Ich starte den Timer")
    time.sleep(duration)

def execute_skill(action, values):
    print(values["number"])
    duration = int(values["number"])  # Wert in eine Ganzzahl konvertieren
    unit = values["unit"]

    if unit == "sekunden":
        sleep(duration)  
    elif unit == "minuten":
        sleep(duration * 60)
    elif unit == "stunden":
        sleep(duration * 60 * 60)
    elif unit == "tage":
        sleep(duration * 60 * 60 * 24)
    else:
        return "Ungültige Einheit!"

    return "Der Timer ist abgelaufen!"

if __name__ == "__main__":
    action = "start_timer"
    values = {"number": "5", "unit": "Sekunden"}

    result = execute_skill(action, values)
    print(result)
