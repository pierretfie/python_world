import requests
import os
import json


#fetch location using ip address 
HOME = os.path.expanduser("~")
locations_path = os.path.join(HOME, "locations.json")
def get_location_by_ip_fallback():
    """Using ip-api.com - unlimited requests but less reliable"""
    try:
        response = requests.get('http://ip-api.com/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            latitude = data.get('lat')
            longitude = data.get('lon')
            city = data.get('city')
            country = data.get('country')
            try:
                with open(locations_path, 'r') as file:
                    save_location = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                save_location = []    
            location_details = {
            'location': f'IP location: {city}, {country}',
            'location_type': None,
            'latitude': latitude,
            'longitude': longitude
        }
            save_location.append(location_details)
            with open(locations_path, 'w') as file:
                json.dump(save_location, file, indent=2)
            return latitude, longitude, city, country
        else:
            print(f"Error: Status code {response.status_code}")
            return None, None, None, None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None, None,None
    
    
    
if __name__ == '__main__':  
    latitude, longitude, city, country = get_location_by_ip_fallback()
