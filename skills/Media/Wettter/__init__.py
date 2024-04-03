
import requests
from datetime import datetime
import os

def execute_skill(action, values):
    print(values)
    print("#######################")
    now = datetime.now()
    current_hour = now.strftime("%H")
    current_minute = now.strftime("%M")
    time_string = f"Es ist {current_hour} Uhr und {current_minute} Minuten."

    api_key = os.getenv("OPEN_WEATHER_MAP_KEY")
    city_name =  "Nuremberg"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        current_temperature = main["temp"]
        
        return f"{time_string} Die aktuelle Temperatur in {city_name} ist {current_temperature} Grad Celsius."
    else:
        return f"{time_string} Die Wetterinformationen konnten nicht abgerufen werden."

if __name__ == "__main__":
    print(execute_skill("", {}))
