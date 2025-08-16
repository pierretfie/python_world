import os
import requests
import json

def get_weather(city_name: str):
    """
    Fetch current weather data for a given city using OpenWeather API.
    Reads API key from the OW_KEY environment variable.
    """
    api_key = os.getenv("OW_KEY")
    if not api_key:
        raise ValueError("❌ API key not found. Please set OW_KEY environment variable.")

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"  # "imperial" for Fahrenheit
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()

        # ✅ Debug: show request URL
        print(f"\n📡 Request URL: {response.url}\n")

        # ✅ Print raw JSON for debugging (pretty formatted)
        data = response.json()
        print("📦 Raw JSON response:")
        print(json.dumps(data, indent=2), "\n")

        # ✅ Extract key weather details
        weather = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
        return weather

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Error occurred: {err}")

    return None


if __name__ == "__main__":
    city = "New York"
    weather_data = get_weather(city)
    if weather_data:
        print("✅ Formatted Weather Summary:")
        print(f"🌍 City: {weather_data['city']}")
        print(f"🌡️ Temperature: {weather_data['temperature']} °C")
        print(f"💧 Humidity: {weather_data['humidity']}%")
        print(f"☁️ Weather: {weather_data['weather']}")
        print(f"💨 Wind Speed: {weather_data['wind_speed']} m/s")
