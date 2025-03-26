import requests
from time import sleep
import random 
import json
import os

HOME = os.path.expanduser("~")
locations_path = os.path.join(HOME, "locations.json")
def search_location(query):
    """
    Search for any location using Nominatim
    Returns a list of matching locations with their details
    """
    # Encode the query to handle special characters
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': query,
        'format': 'json',
        'limit': 5,  # Get top 5 results
        'addressdetails': 1  # Include detailed address data
    }
    
    headers = {
        'User-Agent': 'YourApp/1.0'  # Required by Nominatim's terms
    }
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        results = response.json()
        
        locations = []
        for result in results:
            location = {
                'display_name': result['display_name'],
                'latitude': float(result['lat']),
                'longitude': float(result['lon']),
                'type': result['type'],
                'address': result['address']
            }
            locations.append(location)
            
        return locations
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location: {e}")
        return None
    
    finally:
        # Respect Nominatim's usage policy (max 1 request per second)
        sleep(1)

# Example usage
def get_one_location():
    query = input('Add your Location: ')
    city = input('Add your city: ')
    locations = search_location(query)
    if not locations:
        print("No locations found or error occurred")
        return
        
    loc = random.choice(locations)
    loc_name = loc['display_name']
    loc_type = loc['type']
    coordinates = loc['latitude'], loc['longitude']

    try:
        with open(locations_path, 'r') as file:
            save_location = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        save_location = []    
    if city.lower() in loc['display_name'].lower():
        location_details = {
            'location': loc_name,
            'location_type': loc_type,
            'latitude': loc['latitude'],
            'longitude': loc['longitude']
        }
        save_location.append(location_details)
    print(f"\nFound {len(locations)} locations for '{query}':")
    for i, loc in enumerate(locations, 1):
        print(f"{i}. {loc['display_name']}")
    with open(locations_path, 'w') as file:
        json.dump(save_location, file, indent=2)
    
    return loc, loc_name, loc_type, coordinates

def print_locations(query, city):  # Added city parameter
    locations = search_location(query)
    if not locations:
        print("No locations found or error occurred")
        return
        
    print(f"\nFound {len(locations)} locations for '{query}':")
    for i, loc in enumerate(locations, 1):
        if city.lower() in loc['display_name'].lower():
            print(f"{i}. {loc['display_name']}")
            print(f"   Type: {loc['type']}")
            print(f"   Coordinates: ({loc['latitude']}, {loc['longitude']})")


if __name__ == '__main__':
    get_one_location()
    