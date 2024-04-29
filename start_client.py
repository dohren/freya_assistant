from common import GoogleSpeechRecognition
from common import WakewordDetection
from common import OpenaiTTS
import socketio

wakeword_detection = WakewordDetection()
speech_recognizer = GoogleSpeechRecognition()
openai_tts = OpenaiTTS()

def run_voice_assistant():
    sio = socketio.Client()

    @sio.event
    def connect():
        print('Connected to server')
        openai_tts.speak("Guten Tag, mein Name ist Frehja. Die Sprachsteuerung ist aktiviert. Das konfigurierte Wakeword lautet - hey freya -. Bitte warte auf das akkustische Signal nach dem Wakeword, bevor du mit mir sprichst")

    @sio.event
    def utterance_response(data):
        print('Received utterance response:', data)
        openai_tts.speak(data["response"])

    sio.connect('http://localhost:5000')

    wakeword_detection.daemon = True
    wakeword_detection.start()
    
    while True:
        utterance = None

        if wakeword_detection.wake_word_detected.is_set():
            utterance = speech_recognizer.recognize_speech()
            wakeword_detection.wake_word_detected.clear()
            
        if utterance:
            sio.emit('utterance', { 'utterance': utterance })
       
if __name__ == "__main__":
    run_voice_assistant()