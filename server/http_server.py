from flask import Flask, request, jsonify
from assistant import SkillCrawler, SkillWorker
from common import OpenaiTTS


class IntentFlaskServer:
    def __init__(self,  host='localhost', port=5000):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.skill_crawler = SkillCrawler("skills")
        self.skill_worker = SkillWorker()
        openai_tts = OpenaiTTS()
        openai_tts.speak("Hi, ich bin Frehja. Wie kann ich dir helfen?")

        @self.app.route('/intent', methods=['POST'])
        def handle_intent():
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            try:
                values = data['values']
                action = data['action']
                intent_request = self.skill_crawler.find_intent_by_action(action, values)             
                response = self.skill_worker.execute(intent_request)
                return jsonify({"status": "success", "message": "Intent processed", "response": response}), 200
            except KeyError as e:
                return jsonify({"error": f"Missing key: {e}"}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.app.route('/utterance', methods=['POST'])
        def handle_utterance():
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            if 'utterance' not in data:
                return jsonify({"error": "Missing 'utterance' key"}), 400
            print(data['utterance'])
            utterance = data['utterance']
            intent_request = self.skill_crawler.find_intent_by_utterance(utterance)
            response = self.skill_worker.execute(intent_request)
            return jsonify({"status": "success", "message": f"Received utterance: '{utterance}'"}), 200


    def run(self):
        self.app.run(debug=True, host=self.host, port=self.port, use_reloader=False)

if __name__ == "__main__":
    flask_server = IntentFlaskServer()
    flask_server.run()
