import os 
import sys
from plyer import notification
import platform
import json
from get_location_by_IP import get_location_by_ip_fallback
from datetime import datetime
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from time import sleep



HOME = os.path.expanduser("~")
locations_path = os.path.join(HOME, "locations.json")
script_path = os.path.expanduser('~/Desktop/AI')
sys.path.append(script_path)
# Get the actual home directory path
weather_path = os.path.join(HOME, "weather.json")

def get_weather():
    try:
        with open(locations_path,'r') as file:
            saved_location = json.load(file)
            saved_location = saved_location[-1]
            location_name = saved_location['location']
            latitude = saved_location['latitude']
            longitude = saved_location['longitude']
            print(latitude, longitude)
    except (FileNotFoundError, json.JSONDecodeError):
        text = 'Using IP location'
        location_name = get_location_by_ip_fallback()[2]
        latitude = get_location_by_ip_fallback()[0]
        longitude = get_location_by_ip_fallback()[1]    
    

    # Setup the Open-Meteo API client with cache and retry on error
    cache_path = "/var/tmp/weather_cache/cache.sqlite"
    os.makedirs("/var/tmp/weather_cache", exist_ok=True)
    cache_session = requests_cache.CachedSession(cache_path, expire_after=3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": ["temperature_2m_max", "uv_index_max", "rain_sum", "showers_sum", "precipitation_probability_max"],
        "timezone": "Africa/Cairo",
        "forecast_days": 4
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
    daily_uv_index_max = daily.Variables(1).ValuesAsNumpy()
    daily_rain_sum = daily.Variables(2).ValuesAsNumpy()
    daily_showers_sum = daily.Variables(3).ValuesAsNumpy()
    daily_precipitation_probability_max = daily.Variables(4).ValuesAsNumpy()
    daily_precipitation_sum = daily.Variables(3).ValuesAsNumpy()

    daily_data = {"date": pd.date_range(
        start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
        end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = daily.Interval()),
        inclusive = "left"
    )}

    try:
        with open(weather_path,'r')as file:
            weather = json.load(file)
    except (FileNotFoundError, EOFError, json.JSONDecodeError):
        weather = []
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["uv_index_max"] = daily_uv_index_max
    daily_data["rain_sum"] = daily_rain_sum
    daily_data["showers_sum"] = daily_showers_sum
    daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
    daily_data["precipitation_sum"] = daily_precipitation_sum



    dates = list(daily_data["date"])
    dates = [d.strftime('%Y-%m-%d') for d in daily_data["date"]]
    dates.pop(0)
    max_temp = list(daily_temperature_2m_max)
    max_temp.pop(0)
    precip_prob = list(daily_precipitation_probability_max)
    precip_prob.pop(0)
    precip = list(daily_precipitation_sum)
    precip.pop(0)
    max_uv = list(daily_uv_index_max)
    max_uv.pop(0)
    rain_sum = list(daily_rain_sum)
    rain_sum.pop(0)
    showers_sum = list(daily_showers_sum)
    showers_sum.pop(0)
    days = []
    for date in dates:
        day = datetime.strptime(date, '%Y-%m-%d').strftime('%A')
        days.append(day)


    for a, b, c, d, e, f, g, h in zip(days, dates, max_temp, max_uv, rain_sum, showers_sum,  precip_prob, precip):

        daily_weather ={
        'day' : a,
        'date' : b,
        'max_temp' : round(float(c), 2),
        'max_uv' : round(float(d), 2),
        'rain_sum' : round(float(e), 2),
        'shower_sum' : round(float(f),2),
        'prec_prob_max' : round(float(g),2),
        'precip_sum' : round(float(h)),
        }
        weather.append(daily_weather)
    # daily_dataframe = pd.DataFrame(data = daily_data)
    # print(daily_dataframe)
    with open(weather_path, 'w') as f:
        json.dump(weather, f, indent=2)
    return location_name

def analyze_weather(data):
    temp = data.get("max_temp", 0)  # Max temperature in °C
    rain_sum = data.get("rain_sum", 0)  # Total rainfall in mm
    shower_sum = data.get("shower_sum", 0)  # Total showers in mm
    precip = data.get("precip_sum", 0)  # Total precipitation in mm
    pop_max = data.get("prec_prob_max", 0)  # Max precipitation probability in %
    uv_index = data.get("max_uv", 0)  # UV Index
    
    weather_report = []
    
    # Temperature Analysis
    if temp > 40:
        weather_report.append(f"🌡️ {temp}°C - Extreme heat! Stay hydrated")
    elif temp > 30:
        weather_report.append(f"🌡️ {temp}°C - Hot. Keep hydrated")
    elif temp > 20:
        weather_report.append(f"🌡️ {temp}°C - Warm and pleasant")
    elif temp > 10:
        weather_report.append(f"🌡️ {temp}°C - Cool. Light jacket needed")
    else:
        weather_report.append(f"🌡️ {temp}°C - Cold. Bundle up")
    
    # Rain Analysis
    if rain_sum > 50 or precip > 50:
        weather_report.append(f"🌧️ Severe storm! {rain_sum}mm rain")
    elif rain_sum > 10 or precip > 10:
        weather_report.append(f"🌧️ Heavy rain: {rain_sum}mm. Bring umbrella")
    elif rain_sum > 2 or precip > 2:
        weather_report.append(f"🌧️ Light rain: {rain_sum}mm")
    else:
        weather_report.append("🌧️ No rain expected")
    
    # Shower Analysis
    if shower_sum > 10:
        weather_report.append(f"🚿 Heavy showers: {shower_sum}mm")
    elif shower_sum > 2:
        weather_report.append(f"🚿 Light showers: {shower_sum}mm")
    elif shower_sum > 0:
        weather_report.append(f"🚿 Slight showers: {shower_sum}mm")
    
    # Rain Probability
    if pop_max > 80:
        weather_report.append(f"☔ {pop_max}% chance of rain - Very likely")
    elif pop_max > 50:
        weather_report.append(f"☔ {pop_max}% chance of rain - Likely")
    elif pop_max > 20:
        weather_report.append(f"☔ {pop_max}% chance of rain - Possible")
    else:
        weather_report.append(f"☔ {pop_max}% chance of rain - Unlikely")
    
    # UV Index
    if uv_index > 10:
        weather_report.append(f"☀️ UV: {uv_index} - Extreme! Use sunscreen")
    elif uv_index > 7:
        weather_report.append(f"☀️ UV: {uv_index} - Very high")
    elif uv_index > 5:
        weather_report.append(f"☀️ UV: {uv_index} - Moderate")
    else:
        weather_report.append(f"☀️ UV: {uv_index} - Low")
    
    return " | ".join(weather_report)


# Analyze weather and print insights
def send_notification():
    try:
        with open(locations_path,'r') as file:
            text = ''
            saved_location = json.load(file)
            saved_location = saved_location[-1]
            location_name = saved_location['location']
            location = location_name
            location_type = saved_location['location_type']
            if location_type is not None:
                get_weather()
            sleep(3)
    except (FileNotFoundError, json.JSONDecodeError):
        text = 'Using IP location:'
        location_name = get_location_by_ip_fallback()[2]  
        location = location_name   
        get_weather()
    
    while True:  # Keep checking until we get today's forecast
        try:
            with open(weather_path, 'r') as file:
                forecast = json.load(file)
        except (FileNotFoundError, EOFError, json.JSONDecodeError):
            get_weather()
            continue  # Try reading the file again after fetching

        today = datetime.now().strftime('%Y-%m-%d')

        found = False
        same_day = []
        for data in forecast:
            if today == data['date']:
                same_day.append(data)
        data = same_day[-1]
        found = True
        analysis = analyze_weather(data)
        
        # Format the location header
        location_header = f"📍 {text} {location}".strip()
        
        # Format the message with proper line breaks
        message = f"{location_header}\n\n{analysis}"
        
        notification.notify(
            title="🌤️ Weather Wizard",
            message=message,
            timeout=300
        )

        if platform.system() == 'Linux':
            try:
                os.system('paplay /usr/share/sounds/freedesktop/stereo/message-new-instant.oga')
            except Exception:
                pass
        elif platform.system() == 'Windows':
            try:
                import winsound
                winsound.MessageBeep()
            except Exception:
                pass

        # If today's weather is found, exit the loop
        if found:
            break
        
        # If today's weather is not found, fetch data again
        get_weather()
        sleep(5)  # Wait for a few seconds before retrying

if __name__ == '__main__':
    send_notification()

