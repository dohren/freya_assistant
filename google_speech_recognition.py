import speech_recognition as sr
import playsound
class GoogleSpeechRecognition:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microhpone = sr.Microphone()

    def recognize_speech(self):    
        with self.microhpone as source: 
            audio = self.recognizer.adjust_for_ambient_noise(source)
            playsound.playsound('resources/ping.mp3', True) 
            print("Sprechen Sie jetzt...")
            audio = self.recognizer.listen(source)
        try:
            print("Transkription: ", self.recognizer.recognize_google(audio, language="de-DE"))
            return self.recognizer.recognize_google(audio, language="de-DE")
        except sr.UnknownValueError:
            print("Sprache konnte nicht erkannt werden")
        except sr.RequestError as e:
            print("Fehler bei der Spracherkennung; {0}".format(e))

        return ""
    
if __name__ == "__main__":
    speech_rec = GoogleSpeechRecognition()
    speech_rec.recognize_speech()
