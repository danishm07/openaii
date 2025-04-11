from dotenv import load_dotenv
import os
import requests
import json
from openai import OpenAI
from geopy.geocoders import Nominatim

load_dotenv()

key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=key)


def get_current_weather(latitude, longitude, unit = "fahrenheit"):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&temperature_unit={unit}"
    print(url) 
    response = requests.get(url)
    print(response.text) 
    if response.status_code == 200:
        data = response.json()
        weather = {
            "temperature": data["current_weather"]["temperature"],
            "wind_speed": data["current_weather"]["windspeed"],
            "wind_direction": data["current_weather"]["winddirection"],
            "time": data["current_weather"]["time"]
        }
        return json.dumps(weather)
    else:
        return f"Error: {response.status_code}"


def format_weather_output(json_string):
    """Formats the weather JSON string into a user-friendly message. json.loads returns python dictionary"""
    try:
        weather_data = json.loads(json_string)  # Parse the JSON string
        temperature = weather_data.get("temperature")
        wind_speed = weather_data.get("wind_speed")
        wind_direction = weather_data.get("wind_direction")
        time = weather_data.get("time")

        formatted_message = (
            f"\n"
            f"  Temperature: {temperature}°C\n"
            f"  Wind Speed: {wind_speed} m/s\n"
            f"  Wind Direction: {wind_direction}°\n"
            f"  Time: {time}"
        )
        return formatted_message

    except (json.JSONDecodeError, AttributeError, KeyError) as e:
        return f"Error formatting weather data: {e}"


json_weather = get_current_weather(52.52, 13.41)
weather = format_weather_output(json_weather)

print(f"Curent weather in  Berlin: {weather}")