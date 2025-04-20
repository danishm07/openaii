from dotenv import load_dotenv
import os
import requests
import json
from openai import OpenAI
from geopy.geocoders import Nominatim

load_dotenv()

key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=key)


#function being used to call open meteo api
def get_current_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":latitude,
        "longitude": longitude,
        "current_weather": True
    }
    response = requests.get(url, params = params)
    if response.status_code == 200:
        data = response.json()
        weather = data.get("current_weather", {})
        return{
            "temperature": weather.get("temperature"),
            "windspeed": weather.get("windspeed"),
            "winddirection": weather.get("winddirection"),
            "time": weather.get("time")
        }
    else:
        return {"error": f"Failed to fetch weather data. Status code: {response.status_code}"}
    
functions = [
    {
        "name":"get_current_weather",
        "description": "Get the current weather using latitutde and longitude",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "Latitude of the location"
                },
                "longitude": {
                    "type": "number",
                    "description": "Longitude of the location"
                }
            },
            "required": ["latitude", "longitude"]
        }
    }
]


#using openai to get weather (combining it with openmeteo api function above)
def chat_with_openai(user_query):
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user", "content": user_query}],
        functions = functions,
        function_call = "auto",
    )


    message = response.choices[0].message

    if message.function_call is not None:
        function_name = message.function_call.name
        arguments = message.function_call.arguments

        import json
        args = json.loads(arguments)

        if function_name == "get_current_weather":
            function_response = get_current_weather(
                latitude = args.get("latitude"), 
                longitude = args.get("longitude")
            )

            second_response = client.chat.completions.create(
                model = "gpt-3.5-turbo",
                messages = [
                    {"role": "user", "content": user_query},
                    message,
                    {
                        "role": "function",
                        "name": function_name,
                        "content": str(function_response)
                    }
                ]
            )

            print(second_response.choices[0].message.content)
        else:
            print("Unknown function")
    else:
        print(message["content"])


if __name__ == "__main__":
    user_question = "What's the current weather at latitude 40.7128 and longitude -74.0060?"
    chat_with_openai(user_question)