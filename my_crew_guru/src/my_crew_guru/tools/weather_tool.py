import os
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class WeatherToolInput(BaseModel):
    location: str = Field(..., description="Location for the weather forecast")
    date: str = Field(..., description="Date for the forecast in YYYY-MM-DD format")

class WeatherTool(BaseTool):
    name: str = "Weather Tool"
    description: str = "Fetches current weather information for a given location"
    args_schema: Type[BaseModel] = WeatherToolInput

    def _run(self, location: str, date: str) -> dict:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": location, "appid": api_key, "units": "metric"}
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code != 200:
            raise ValueError(f"Weather API error: {data.get('message')}")

        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"]
        forecast = f"{temp}°C, {condition}"

        # MUST return dict with key exactly matching tasks.yaml
        return {"forecast": forecast}
