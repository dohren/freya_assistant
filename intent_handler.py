# intent_handler.py

import os
import yaml
import importlib.util

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

    def handle_intent(self, utterance):
        for skill in self.skills:
            for intent in skill.intents:
                cleaned_utterance = utterance.lower().strip() 
                if cleaned_utterance in [u.lower().strip() for u in intent['utterances']]:
                    # Führe die entsprechende Aktion aus
                    action = intent['action']
                    response = skill.execute_skill()
                    return True, response, action
        return False, "", "not_found"
        
if __name__ == "__main__":
    skill_package_path = "skills"
    intent_handler = IntentHandler(skill_package_path)

    utterance= "Schalte das Licht Aus"
    intent_handler.handle_intent(utterance)

    utterance= "musik stoppen"
    intent_handler.handle_intent(utterance)