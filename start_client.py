from common import GoogleSpeechRecognition
from common import WakewordDetection
from common import OpenaiTTS
import time
import socketio
import threading

wakeword_detection = WakewordDetection()
speech_recognizer = GoogleSpeechRecognition()
openai_tts = OpenaiTTS()

def run_voice_assistant():
    sio = socketio.Client()
    speaking_event = threading.Event()

    @sio.event
    def connect():
        print('Connected to server')
        openai_tts.speak("Guten Tag, mein Name ist Frehja.")
        openai_tts.speaking_event.wait()

    @sio.event
    def utterance_response(data):
        print('Received utterance response:', data)
        speaking_event.set()  # Indicate that speaking has started
        openai_tts.speak(data["response"])
        openai_tts.speaking_event.wait()
        speaking_event.clear()  # Indicate that speaking has ended


    @sio.event
    def message(data):
        print(data["message"])

    sio.connect('http://localhost:5000/?username=freya')

    wakeword_detection.daemon = True
    wakeword_detection.start()

    while True:
        utterance = None

        if wakeword_detection.wake_word_detected.is_set() and not speaking_event.is_set():
            utterance = speech_recognizer.recognize_speech()
            wakeword_detection.wake_word_detected.clear()

        if utterance:
            sio.emit('chatgpt', {'utterance': utterance})
            
        if speaking_event.is_set():
            wakeword_detection.wake_word_detected.clear()

        time.sleep(1)

if __name__ == "__main__":
    run_voice_assistant()