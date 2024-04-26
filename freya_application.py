from google_stt import GoogleSpeechRecognition
from sphinx_wakeword import WakewordDetection
from skill_crawler import SkillCrawler
from openai_tts import OpenaiTTS
from skill_worker import SkillWorker
from http_server import IntentFlaskServer
import time
import sys
import threading

wakeword_detection = WakewordDetection()
speech_recognizer = GoogleSpeechRecognition()
skill_crawler = SkillCrawler("skills")
openai_tts = OpenaiTTS()
skill_worker = SkillWorker()

# Create the Flask server instance with the skill worker
flask_server = IntentFlaskServer(skill_crawler, skill_worker)

def run_voice_assistant():
    wakeword_detection.daemon = True 
    wakeword_detection.start()    
    openai_tts.speak("Hi, ich bin Frehja. Wie kann ich dir helfen?")

    while True:
        utterance = None
        intent_request = None

        if wakeword_detection.wake_word_detected.is_set():
            utterance = speech_recognizer.recognize_speech()
            wakeword_detection.wake_word_detected.clear()
            
        if utterance:
            intent_request = skill_crawler.find_intent(utterance)
            
        if intent_request:
            skill_worker.execute(intent_request)
            time.sleep(3)

        if intent_request and intent_request.action == "exit":
           time.sleep(5)
           break
       
        time.sleep(1)
    
    sys.exit()

if __name__ == "__main__":
    voice_thread = threading.Thread(target=run_voice_assistant)
    voice_thread.start()
    flask_server.run()



