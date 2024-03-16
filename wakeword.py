import pvporcupine
from pvrecorder import PvRecorder
import os

class WakewordDetection:
    def __init__(self, keywords, keyword_paths, model_path):
        self.keywords = keywords
        self.access_key = os.getenv("PORCUPINE_ACCESS_KEY")
        self.keyword_paths = keyword_paths
        self.model_path = model_path
        self.porcupine = None
        self.recorder = None
    
    def setup(self):
        #for keyword in pvporcupine.KEYWORDS:
        #    print(keyword)
        
        self.porcupine = pvporcupine.create(access_key=self.access_key, keyword_paths=self.keyword_paths, model_path=self.model_path)
        self.recorder = PvRecorder(device_index=-1, frame_length=self.porcupine.frame_length)
    
    def detect_wakeword(self):
        try:
            self.recorder.start()

            while True:
                keyword_index = self.porcupine.process(self.recorder.read())
                if keyword_index >= 0:
                    print(f"Detected {self.keywords[keyword_index]}")
                    break

        except KeyboardInterrupt:
            self.recorder.stop()
        
        return True

    def cleanup(self):   
            self.porcupine.delete()
            self.recorder.delete()

if __name__ == "__main__":
    keywords = ["hey freya"]
    keyword_paths = ['resources/freya.ppn']
    model_path = 'resources/porcupine_params_de.pv'
    
    wakeword_detection = WakewordDetection(keywords, keyword_paths, model_path)
    wakeword_detection.setup()
    wakeword_detection.detect_wakeword()