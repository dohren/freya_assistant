import speech_recognition as sr
import subprocess
import struct
import pyaudio
import pvporcupine
import os

GOOGLE_CLOUD_SPEECH_CREDENTIALS = r'{put service account key json}'

r = sr.Recognizer()
m = sr.Microphone()

porcupine = None
sound = None
audio_stream = None

access_key = os.getenv("PORCUPINE_ACCESS_KEY")
keywords = ["hey freya"]
keyword_paths = ['resources/freya.ppn']
model_path = 'resources/porcupine_params_de.pv'

def talk(texte):
    #tts = gTTS(text=texte, lang='en', lang_check=False)
    #tts.save("text.mp3")
    #subprocess.Popen(["mpg321", "text.mp3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(texte)

try:
    talk("I am ready")
    porcupine = pvporcupine.create(access_key=access_key, keyword_paths=keyword_paths, model_path=model_path)

    sound = pyaudio.PyAudio()
    
    audio_stream = sound.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)
    
    with m as source: r.adjust_for_ambient_noise(source)
    
    listening = False
    
    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)
        
        if keyword_index >= 0:
            listening = True
            print("Hotword Detected")
            
        if listening:
            with m as source: audio = r.listen(source)
            try:
                #value = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
                value = r.recognize_google(audio)
                print("You said {}".format(value))
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
            except sr.RequestError as e:
                print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
            finally:
                listening = False
            
except KeyboardInterrupt:
    print("Stopping....")

finally:
    if porcupine is not None:
        porcupine.delete()

    if audio_stream is not None:
        audio_stream.close()

    if sound is not None:
        sound.terminate()