from openai_tts import OpenaiTTS

def execute_skill(action, values):
    tts = OpenaiTTS()
    something = values["something"]
    tts.speak(f"Hello {something}") 