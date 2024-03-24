from openai import OpenAI
from openai_tts import OpenaiTTS

def execute_skill(action, values):
        recognized_text = values["recognized_text"]
        
        if recognized_text:
            openai_tts = OpenaiTTS()
            openai_tts.synthesize_speech("Gib mir bitte einen Moment, ich überlege")
            client = OpenAI()
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                    {"role": "system", "content": "Du bist mein persönlicher Asisstent und Berater. Deine Antwort reduziert sich auf maximal 3 Sätze"},
                    {"role": "user", "content": recognized_text}
                ]
            )
            return completion.choices[0].message.content

        return "Das habe ich nicht verstanden"