import os
import yaml
import importlib.util
import re
from assistant.intent_request import IntentRequest

class SkillCrawler:

    VARIABLE_PATTERN = pattern = r'\{(.+?)\}' 


    def __init__(self, skill_package_path):
        self.skills = []
        self.intents = []
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
                self.append_skill(skill_module, intents_file)
                

    def append_skill(self, skill_module, intents_file):
        with open(intents_file, 'r') as file:
            intents_data = yaml.safe_load(file)
            intents = intents_data.get('intents', [])
            skill_module.intents = intents
            for intent in intents:
                self.intents.append(intent)
                if intent["action"] == "fallback": 
                    self.fallback_skill = skill_module
    
        self.skills.append(skill_module)
       
                

    def find_intent_by_utterance(self, recognized_text):
        values = {"recognized_text": recognized_text}

        for skill in self.skills:
            for intent in skill.intents:
                for utterance in intent['utterances']:
                    cleaned_recognized_text = recognized_text.lower().strip()
                    cleaned_utterance = utterance.lower().strip()
                    if cleaned_recognized_text == cleaned_utterance:
                        action = intent['action']
                        return IntentRequest(skill, values, action)
                    
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
                        return IntentRequest(skill, values, action)

        return IntentRequest(self.fallback_skill, values, "default")


    def find_intent_by_action(self, action, values):
        for skill in self.skills:
            for intent in skill.intents:
                if action == intent["action"]:
                    return IntentRequest(skill, values, action)
        return IntentRequest(self.fallback_skill, values, "default")

    def get_intents(self):
        return self.intents

if __name__ == "__main__":
    skill_package_path = "skills"
    skill_crawler = SkillCrawler(skill_package_path)

    utterance= "Spiele Musik"
    intent_request = skill_crawler.find_intent_by_utterance(utterance)
    print(intent_request.values)

    utterance= "Schalte das Licht im Wohnzimmer aus"
    intent_request = skill_crawler.find_intent_by_utterance(utterance)
    print(intent_request.values)

    utterance= "Schalte das Licht ganz aus"
    intent_request = skill_crawler.find_intent_by_utterance(utterance)
    print(intent_request.values)

    utterance= "Wie wird das Wetter heute"
    intent_request = skill_crawler.find_intent_by_utterance(utterance)
    intent_request.skill.execute_skill(intent_request.action, intent_request.values)
    print(intent_request.values)

    intent_request = skill_crawler.find_intent_by_action("get_weather", [])
    intent_request.skill.execute_skill(intent_request.action, intent_request.values)
    