from assistant.intent_request import IntentRequest

class SkillWorker:
    def execute(self, intent_request):
        print(intent_request)
        result = intent_request.skill.execute_skill(intent_request.action, intent_request.values)
        return result

if __name__ == "__main__":
    app = SkillWorker()
    intent_request = IntentRequest(10, '{"test": "test"}', "Task1")
    app.execute(intent_request)
