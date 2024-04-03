import threading
from intent_request import IntentRequest

class SkillWorker:
    def __init__(self):
        self.threads = {}
        self.stop_events = {}

    def execute(self, intent_request):
        key = intent_request.action
        # Wenn bereits ein Thread für diesen Key läuft, stoppe ihn zuerst
        if intent_request.action in self.threads:
            self.stoppe_thread(key)

        # Zurücksetzen des Stop-Events für den neuen Thread
        stop_event = threading.Event()
        self.stop_events[key] = stop_event

        # Starte einen neuen Thread
        thread = threading.Thread(target=self.run_skill, args=(key, intent_request, stop_event))
        self.threads[key] = thread
        thread.start()

    def stoppe_thread(self, key):
        # Setze das Stop-Event und warte auf die Beendigung des Threads, falls vorhanden
        if key in self.stop_events:
            self.stop_events[key].set()
        if key in self.threads:
            self.threads[key].join()
            self.aufraeumen(key)

    def run_skill(self, key, intent_request, stop_event):
        print(f"Thread {key} gestartet.")
        intent_request.skill.execute_skill(key, intent_request.values)

        self.aufraeumen(key)
        print(f"Thread {key} beendet.")

    def aufraeumen(self, key):
        # Entferne den Thread und das Stop-Event aus den Dictionaries
        if key in self.threads:
            del self.threads[key]
        if key in self.stop_events:
            del self.stop_events[key]
        # Überprüfe, ob noch weitere Threads laufen
        if not self.threads:
            print("Alle Threads beendet.")

if __name__ == "__main__":
    app = SkillWorker()
    intent_request = IntentRequest(10, '{"test": "test"}', "Task1")
    app.execute(intent_request)
