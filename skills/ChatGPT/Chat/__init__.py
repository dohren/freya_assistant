import sys
import os.path
from openai import OpenAI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from openai_tts import OpenaiTTS

def execute_skill(action, values):
        recognized_text = values["recognized_text"]
        
        if recognized_text:
            tts = OpenaiTTS()
            tts.speak("Gib mir bitte einen Moment, ich überlege")
            client = OpenAI()
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                    {"role": "system", "content": "Du bist mein persönlicher Asisstent und Berater. Deine Antwort reduziert sich auf maximal 3 Sätze"},
                    {"role": "user", "content": recognized_text}
                ]
            )
            tts.speak(completion.choices[0].message.content)

        "Das habe ich nicht verstanden"

if __name__ == "__main__":
      execute_skill("chatgpt", {"recognized_text": "wo wohnt Asterix"})