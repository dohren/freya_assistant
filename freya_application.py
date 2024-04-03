from google_stt import GoogleSpeechRecognition
from sphinx_wakeword import WakewordDetection
from skill_crawler import SkillCrawler
from openai_tts import OpenaiTTS
from skill_worker import SkillWorker
import sys


wakeword_detection = WakewordDetection()
speech_recognizer = GoogleSpeechRecognition()
skill_crawler = SkillCrawler("skills")
openai_tts = OpenaiTTS()
skill_worker = SkillWorker()

result = []

def main():
    wakeword_detection.daemon = True 
    wakeword_detection.start()    
    openai_tts.synthesize_speech("Hi, ich bin Frehja. Wie kann ich dir helfen?")

    while True:
        utterance = None

        if wakeword_detection.wake_word_detected.is_set():
            wakeword_detection.wake_word_detected.clear()
            utterance = speech_recognizer.recognize_speech()
            
            
        if utterance:
            intent_request = skill_crawler.find_intent(utterance)
            #skill_worker.execute(intent_request)
            

        if len(result) > 0:
           current_result = result.pop(0)
           if current_result.success:
                openai_tts.synthesize_speech(current_result.response)
           else:
                openai_tts.synthesize_speech("Ich habe das nicht verstanden")
           if current_result.action == "exit":
                break
    
    sys.exit()

if __name__ == "__main__":
    main()



