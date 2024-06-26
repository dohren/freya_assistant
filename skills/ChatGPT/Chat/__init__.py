from openai import OpenAI

def execute_skill(action, values):   
        recognized_text = values["recognized_text"]
        
        if recognized_text:
            client = OpenAI()
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                    {"role": "system", "content": "Du bist mein persönlicher Asisstent mit dem Namen Freya. Deine Antwort reduziert sich auf maximal 3 Sätze. Bitte duze mich."},
                    {"role": "user", "content": recognized_text}
                ]
            )
            return completion.choices[0].message.content

if __name__ == "__main__":
      execute_skill("chatgpt", {"recognized_text": "wo wohnt Asterix"})