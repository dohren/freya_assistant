
class Chatgpt:
    base_instruction="""Ich möchte eine Heimautomatisierung nutzen. Bitte unterscheide zwischen Befehlen und normaler Konversation. Wenn du einen Befehl erhältst, der einem aus der folgenden 
Liste ähnelt, schreibe '#command:' davor und setze die entsprechende Utterance dahinter. Dies ist nur eine Anweisung für die folgende Konversation. 
Antworte auf diesen Prompt bitte nur mit 'OK'."""

    def get_chtgpt_intructions(self, intents):
        intent_string = '\n'.join(['; '.join([f'{key}: {value}' for key, value in d.items()]) for d in intents])
        instructions = self.base_instruction + "\n\n" + intent_string
        return instructions
