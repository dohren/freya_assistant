from google_stt import GoogleSpeechRecognition
from wakeword import WakewordDetection
#from logging import configure_logging
from intent_handler import IntentHandler
from openai_tts import OpenaiTTS


def main():
    keywords = ["hey freya"]
    keyword_paths = ['resources/freya.ppn']
    model_path = 'resources/porcupine_params_de.pv'
    #configure_logging()

    speech_recognizer = GoogleSpeechRecognition()
    intent_handler = IntentHandler("skills")

    openaiTTS = OpenaiTTS()

    wakeword_detection = WakewordDetection(keywords, keyword_paths, model_path)
    wakeword_detection.start()    

    utterance = None
    
    while True:
            if wakeword_detection.wake_word_detected.is_set():
                utterance = speech_recognizer.recognize_speech()
                wakeword_detection.wake_word_detected.clear()

            if utterance:
                success, response, action = intent_handler.handle_intent(utterance)
                if success:
                    openaiTTS.synthesize_speech(response)
                else:
                    openaiTTS.synthesize_speech("Ich habe das nicht verstanden")
                utterance = None
                if action == "exit":
                    break

    wakeword_detection.stop()

if __name__ == "__main__":
    main()

