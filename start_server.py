from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from assistant import SkillCrawler, SkillWorker

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'  # Replace with your secret key
socketio = SocketIO(app)

skill_crawler = SkillCrawler("skills")
skill_worker = SkillWorker()

initialized = False

clients = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    user_info = request.args.get('username')
    clients[user_info] = request.sid

@socketio.on('intent_request')
def handle_intent_request(data):
    if not data or 'values' not in data or 'action' not in data:
        emit('error', {'error': 'Invalid intent request'})
        return
    values = data['values']
    action = data['action']
    intent_request = skill_crawler.find_intent_by_action(action, values)
    response = skill_worker.execute(intent_request)
    emit('intent_response', {'status': 'success', 'message': 'Intent processed', 'response': response})


@app.route('/intent', methods=['POST'])
def post_intent():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    try:
        values = data['values']
        action = data['action']
        intent_request = skill_crawler.find_intent_by_action(action, values)      
        print(action)       
        response = skill_worker.execute(intent_request)
        emit('message', {'message': response}, namespace='/', room=clients["freya"])
        return jsonify({"status": "success", "message": "Intent processed", "response": response}), 200
    except KeyError as e:
        return jsonify({"error": f"Missing key: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@socketio.on('utterance')
def handle_utterance(data):
    if not data or 'utterance' not in data:
        emit('error', {'error': 'Invalid utterance request'})
        return

    utterance = data['utterance']
    intent_request = skill_crawler.find_intent_by_utterance(utterance)
    response = skill_worker.execute(intent_request)
    emit('utterance_response', {
        'status': 'success',
        'message': f"Received utterance: '{utterance}'",
        'response': response
    })

if __name__ == '__main__':   
    socketio.run(app, debug=True)