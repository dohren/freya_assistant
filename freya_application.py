from google_stt import GoogleSpeechRecognition
from sphinx_wakeword import WakewordDetection
from intent_handler import IntentHandler
from openai_tts import OpenaiTTS
import sys
import threading

wakeword_detection = WakewordDetection()
speech_recognizer = GoogleSpeechRecognition()
intent_handler = IntentHandler("skills")
openai_tts = OpenaiTTS()

result = []

def handle_intent_thread(utterance):
    result.append(intent_handler.handle_intent(utterance))

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
            thread = threading.Thread(target=handle_intent_thread, args=(utterance,))       
            thread.start()

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



