from common import GoogleSpeechRecognition
from common import WakewordDetection
from common import OpenaiTTS
import requests
import time
import sys
import json

wakeword_detection = WakewordDetection()
speech_recognizer = GoogleSpeechRecognition()
openai_tts = OpenaiTTS()

def run_voice_assistant():
    wakeword_detection.daemon = True 
    wakeword_detection.start()   
    openai_tts.speak("Guten Tag, mein Name ist Frehja. Die Sprachsteuerung ist aktiviert. Das konfigurierte Wakeword lautet - hey freya -. Bitte warte auf das akkustische Signal nach dem Wakeword, bevor du mit mir sprichst") 

    while True:
        utterance = None
        intent_request = None

        if wakeword_detection.wake_word_detected.is_set():
            utterance = speech_recognizer.recognize_speech()
            wakeword_detection.wake_word_detected.clear()
            
        if utterance:
            url = 'http://localhost:5000/utterance'
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            data = { "utterance": utterance }
            json_data = json.dumps(data, ensure_ascii=False).encode('utf8')
            response = requests.post(url, headers=headers, data=json_data)
            print(response.text)

        if intent_request and intent_request.action == "exit":
           time.sleep(5)
           break
       
        time.sleep(1)
    
    sys.exit()

if __name__ == "__main__":
    run_voice_assistant()