from google_speech_recognition import GoogleSpeechRecognition
from wakeword import WakewordDetection
#from logging import configure_loggingls -l
from intent_handler import IntentHandler
from openai_tts import OpenaiTTS
import os

def main():
    keywords = ["hey freya"]
    keyword_paths = ['resources/freya.ppn']
    model_path = 'resources/porcupine_params_de.pv'
    #configure_logging()

    
    wakeword_detector = WakewordDetection(keywords, keyword_paths, model_path)
    speech_recognizer = GoogleSpeechRecognition()
    intent_handler = IntentHandler("skills")

    openaiTTS = OpenaiTTS()

    while True:
        # Warten auf das Wake-Word
        if wakeword_detector.detect_wakeword():
            # Wenn das Wake-Word erkannt wird, Spracherkennung aktivieren
            utterance = speech_recognizer.recognize_speech()
            # Skill-Auswahl und Verarbeitung des erkannten Textes
            success, response, action = intent_handler.handle_intent(utterance)
            if success:
                openaiTTS.synthesize_speech(response)
            else:
                openaiTTS.synthesize_speech("Ich habe das nicht verstanden")
            if action == "exit":
                break

if __name__ == "__main__":
    main()

