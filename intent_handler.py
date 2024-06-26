import os
import yaml
import importlib.util
import re
from intent_response import IntentResponse

class IntentHandler:

    VARIABLE_PATTERN = pattern = r'\{(.+?)\}' 

    def __init__(self, skill_package_path):
        self.skills = []
        self.skills_dir = skill_package_path
        self.load_skills()

    def load_skills(self):
        skill_dirs = []
        skills_path = os.path.join(os.getcwd(), self.skills_dir)
        for packages_dir in os.listdir(skills_path):
            skill_dir = os.path.join(skills_path, packages_dir)
            skill_dirs.extend([os.path.join(skill_dir, d) for d in os.listdir(skill_dir) if os.path.isdir(os.path.join(skill_dir, d))])

        for skill_dir in skill_dirs:
            init_file = os.path.join(skill_dir, '__init__.py')
            intents_file = os.path.join(skill_dir, 'intents.yaml')

            if os.path.isfile(init_file) and os.path.isfile(intents_file):
                skill_module = importlib.util.module_from_spec(
                    importlib.util.spec_from_file_location(f"{self.skills_dir}.{skill_dir}", init_file))
                importlib.util.spec_from_file_location(f"{self.skills_dir}.{skill_dir}", init_file).loader.exec_module(skill_module)

                with open(intents_file, 'r') as file:
                    intents_data = yaml.safe_load(file)
                    intents = intents_data.get('intents', [])
                    skill_module.intents = intents
                
                self.skills.append(skill_module)

    def handle_intent(self, recognized_text):
        values = {"recognized_text": recognized_text}

        for skill in self.skills:
            for intent in skill.intents:
                for utterance in intent['utterances']:
                    cleaned_recognized_text = recognized_text.lower().strip()
                    cleaned_utterance = utterance.lower().strip()
                    if cleaned_recognized_text == cleaned_utterance:
                        action = intent['action']
                        response = skill.execute_skill(action, {})
                        return IntentResponse(True, response, action)
                    
                    utterance_pattern = "^" + re.sub(self.VARIABLE_PATTERN, r'(.+?)', cleaned_utterance + "$")                    
                    findings = re.findall(utterance_pattern, cleaned_recognized_text)

                    for find in findings:
                        variables = {}
                        variables = re.findall(self.VARIABLE_PATTERN, cleaned_utterance)
                        if isinstance(find, str):
                            values[variables[0]] = find
                        else:
                            for key_index, item in enumerate(find):
                                values[variables[key_index]] = item
                        action = intent['action']
                        response = skill.execute_skill(action, values)
                        return IntentResponse(True, response, action)

        return IntentResponse(False, "", "not_found")

if __name__ == "__main__":
    skill_package_path = "skills"
    intent_handler = IntentHandler(skill_package_path)

    utterance= "Spiele Musik"
    result = intent_handler.handle_intent(utterance)
    print(result.response)

    utterance= "Schalte das Licht im Wohnzimmer aus"
    result = intent_handler.handle_intent(utterance)
    print(result.response)

    utterance= "Schalte das Licht ganz aus"
    result = intent_handler.handle_intent(utterance)
    print(result.response)

    utterance= "Wie wird das Wetter heute"
    result = intent_handler.handle_intent(utterance)
    print(result.response)