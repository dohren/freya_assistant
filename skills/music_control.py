# music_control.py
import os
from intent_handler import IntentHandler

class MusicControlSkill:
    def __init__(self):
        self.intent_handler = IntentHandler(os.path.dirname(__file__))

    def process_command(self, command_text):
        # Führe Intent-Handler für den erkannten Text aus
        self.intent_handler.handle_intent(command_text)