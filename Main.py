import requests, json
from threading import Thread
from dotenv import load_dotenv
import os


class Weather:
    def __init__(self):
        load_dotenv()
        self.url_weather = os.getenv("WEATHER_API_KEY")
        self.url_location = os.getenv("IP_API_KEY")
        self.params = {"latitude": 52.52,
                       "longitude": 13.41,
                       "current":"temperature_2m,weather_code,is_day"}
        #"latitude": 52.52,"longitude": 13.41
        self.data = {
            "current": {
                "temperature_2m": 18.5,
                "weather_code": 61,
                "is_day": 1
            }
        }

    def get_location(self):
        self.location = requests.get(self.url_location).json()
        print(self.location)
        return self.location["latitude"], self.location["longitude"]

    def start_weather(self, on_update=None):
        try:
            with open("data.json", "r") as datei:
                self.data = json.load(datei)
            print("Json geladen")
        except FileNotFoundError:
            self.data = {
                "current": {
                    "temperature_2m": 18.5,
                    "weather_code": 61,
                    "is_day": 1
                }
            }
        thread = Thread(target=self.start_thread,args=(on_update,), daemon=True)
        thread.start()

    def start_thread(self, on_update=None):
        try:
            self.get_location()
            self.params = {"latitude": self.location["latitude"],
                           "longitude": self.location["longitude"],
                           "current": "temperature_2m,weather_code,is_day"}
            print("location geladen")
        except Exception as e:
            print(f"Location-Fehler: {e}")

        self.get_weather_data(on_update)

    def get_weather_data(self, on_update=None):
        try:
            self.data = requests.get(self.url_weather, params=self.params,timeout=5).json()
            with open("data.json", "w") as datei:
                json.dump(self.data, datei)
            print("API geladen",self.data)
        except Exception as e:
            print(f"API-Fehler: {e} ")
        finally:
            if on_update:
                on_update()

    def refresh(self, on_update=None):
        thread = Thread(target=self.get_weather_data, args=(on_update,), daemon=True)
        thread.start()

    def get_temperature(self):
        return self.data["current"]["temperature_2m"]

    def weather_code(self):
        if self.data["current"]["is_day"] == 0:
            return "night"
        elif self.data["current"]["weather_code"] in [0,1]:
            return "sun"
        elif self.data["current"]["weather_code"] in [2,3,4]:
            return "cloud"
        elif self.data["current"]["weather_code"] in [45, 48]:
            return "fog"
        elif self.data["current"]["weather_code"] in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
            return "rain"
        elif self.data["current"]["weather_code"] in [71, 73, 75]:
            return "snow"
        elif self.data["current"]["weather_code"] in [95, 96, 99]:
            return "thunder"
        else: return "unbekannt"

#w= Weather()
#print(w.weather_code())
# try:
#     self.data = requests.get(self.url_weather, params=self.params,timeout=5).json()
#     with open("data.json", "w") as datei:
#         json.dump(self.data, datei)
#         print(self.data)
#     return self.data
# except:
#     try:
#         with open("data.json", "r") as datei:
#             self.data = json.load(datei)
#     except FileNotFoundError:
#         self.data = {
#             "current": {
#                 "temperature_2m": 18.5,
#                 "weather_code": 61
#             }
#         }
#