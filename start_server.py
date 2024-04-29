from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from assistant import SkillCrawler, SkillWorker
from common import OpenaiTTS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'  # Replace with your secret key
socketio = SocketIO(app)

skill_crawler = SkillCrawler("skills")
skill_worker = SkillWorker()
openai_tts = OpenaiTTS()

initialized = False

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect_event')
def handle_connect_event():
    emit('message', 'Server connected')

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