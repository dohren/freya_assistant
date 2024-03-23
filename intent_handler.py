# intent_handler.py

import os
import yaml
import importlib.util
import re

class IntentHandler:
    def __init__(self, skill_package_path):
        self.skills = []
        self.skills_dir = skill_package_path
        self.load_skills()

    def load_skills(self):
        skills_path = os.path.join(os.getcwd(), self.skills_dir)
        skills_subdirs = [d for d in os.listdir(skills_path) if os.path.isdir(os.path.join(skills_path, d))]

        for skill_dir in skills_subdirs:
            init_file = os.path.join(skills_path, skill_dir, '__init__.py')
            intents_file = os.path.join(skills_path, skill_dir, 'intents.yaml')

            if os.path.isfile(init_file) and os.path.isfile(intents_file):
                with open(intents_file, 'r') as file:
                    intents_data = yaml.safe_load(file)
                intents = intents_data.get('intents', [])

                skill_module = importlib.util.module_from_spec(
                    importlib.util.spec_from_file_location(f"{self.skills_dir}.{skill_dir}", init_file))
                importlib.util.spec_from_file_location(f"{self.skills_dir}.{skill_dir}", init_file).loader.exec_module(skill_module)

                # Fügen Sie die Intents zur Skill-Modulinstanz hinzu
                skill_module.intents = intents
                self.skills.append(skill_module)

    def handle_intent(self, recognized_text):

        for skill in self.skills:
            for intent in skill.intents:
                cleaned_recognized_text = recognized_text.lower().strip()
                for utterance in intent['utterances']:
                    cleaned_utterance = utterance.lower().strip()
                    if cleaned_recognized_text == cleaned_utterance:
                        action = intent['action']
                        response = skill.execute_skill(action, {})
                        return True, response, action
                    
                    values = {}
                    variables = {}
                    pattern = r'\{(.+?)\}' 
                    replaced_variable = "^" + re.sub(pattern, r'(.+?)', cleaned_utterance + "$")
                    variables = re.findall(pattern, cleaned_utterance)
                    findings = re.findall(replaced_variable, cleaned_recognized_text)
                    
                    for find in findings:
                        if isinstance(find, str):
                            values[variables[0]] = find
                        else:
                            for key_index, item in enumerate(find):
                                values[variables[key_index]] = item
                        action = intent['action']
                        response = skill.execute_skill(action, values)
                        return True, response, action

        return False, "", "not_found"

if __name__ == "__main__":
    skill_package_path = "skills"
    intent_handler = IntentHandler(skill_package_path)

    utterance= "Spiele Musik"
    success, response, action = intent_handler.handle_intent(utterance)
    print(response)

    utterance= "Schalte das Licht im Wohnzimmer aus"
    success, response, action = intent_handler.handle_intent(utterance)
    print(response)

    utterance= "Schalte das Licht ganz aus"
    success, response, action = intent_handler.handle_intent(utterance)
    print(response)

    utterance= "Wie wird das Wetter heute"
    success, response, action = intent_handler.handle_intent(utterance)
    print(response)