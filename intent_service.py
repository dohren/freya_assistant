from flask import Flask, request, jsonify
import threading
from skill_worker import SkillWorker

app = Flask(__name__)

class IntentRequest:
    def __init__(self, skill, values, action):
        self.skill = skill
        self.values = values
        self.action = action

class IntentService(threading.Thread):
    def __init__(self, skill_worker):
        threading.Thread.__init__(self)
        self.skill_worker = skill_worker

    def run(self):
        app.run(debug=False)

    def process_intent(self, intent):
        self.skill_worker.execute(intent)

    def intent_handler(self):
        data = request.json
        if data and 'skill' in data and 'values' in data and 'action' in data:
            intent = IntentRequest(data['skill'], data['values'], data['action'])
            self.process_intent(intent)
            return jsonify({'message': 'Intent received successfully'}), 200
        else:
            error = {'error': 'Invalid request body'}
            return jsonify(error), 400

intent_service = IntentService(SkillWorker())  # IntentService-Instanz mit SkillWorker-Instanz erstellen

@app.route('/intent', methods=['POST'])
def intent_route():
    return intent_service.intent_handler()

if __name__ == '__main__':
    intent_service.start()

    # Hier kannst du deine Hauptanwendung in einer Schleife laufen lassen
    while True:
        # Füge hier deine Hauptanwendungsfunktionalität hinzu
        pass

