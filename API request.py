import requests


params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "current": "temperature_2m,weather_code,is_day",
    "daily": "temperature_2m_max,temperature_2m_min,weather_code",
    "forecast_days": 7,
    "timezone": "auto"
}

data = requests.get("https://api.open-meteo.com/v1/forecast", params=params).json()
print(data["daily"])