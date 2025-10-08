import os
import requests

class WeatherTool:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/forecast"

    def get_forecast(self, location, date):
        params = {
            "q": location,
            "appid": self.api_key,
            "units": "metric"
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        # Pick forecast closest to the given date
        forecast = next((f for f in data["list"] if f["dt_txt"].startswith(date)), None)
        return forecast
