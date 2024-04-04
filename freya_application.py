from google_stt import GoogleSpeechRecognition
from sphinx_wakeword import WakewordDetection
from skill_crawler import SkillCrawler
from openai_tts import OpenaiTTS
from skill_worker import SkillWorker
import time
import sys


wakeword_detection = WakewordDetection()
speech_recognizer = GoogleSpeechRecognition()
skill_crawler = SkillCrawler("skills")
openai_tts = OpenaiTTS()
skill_worker = SkillWorker()


def main():
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
            skill_worker.execute(intent_request)
            time.sleep(3)
            
        if intent_request and intent_request.action == "exit":
           time.sleep(5)
           break
       
        time.sleep(1)
    
    sys.exit()

if __name__ == "__main__":
    main()



