
from datetime import datetime

def execute_skill(action, values):
    now = datetime.now()
    current_hour = now.strftime("%H")
    current_minute = now.strftime("%M")
    return f"Es ist {current_hour} Uhr und {current_minute} Minuten."