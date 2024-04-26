from flask import Flask, request, jsonify

class IntentFlaskServer:
    def __init__(self, skill_crawler, skill_worker, host='localhost', port=5000):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.skill_worker = skill_worker

        @self.app.route('/intent', methods=['POST'])
        def handle_intent():
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            try:
                values = data['values']
                action = data['action']
                intent_request = skill_crawler.find_skill(action, values)             
                response = self.skill_worker.execute(intent_request)
                return jsonify({"status": "success", "message": "Intent processed", "response": response}), 200
            except KeyError as e:
                return jsonify({"error": f"Missing key: {e}"}), 400
            except Exception as e:
                return jsonify({"error": str(e)}), 500

    def run(self):
        self.app.run(debug=True, host=self.host, port=self.port, use_reloader=False)

