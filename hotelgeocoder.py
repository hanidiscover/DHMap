import pandas as pd
import requests
import time

API_KEY = '!!!!!!!!!!!!!key here'

def geocode_place(name):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': name, 'key': API_KEY}
    response = requests.get(base_url, params=params).json()

    if response['status'] == 'OK':
        loc = response['results'][0]['geometry']['location']
        return loc['lat'], loc['lng']
    else:
        print(f"Failed to geocode: {name} ({response['status']})")
        return None, None

# Load your file (e.g., hotels.csv)
df = pd.read_csv('vancouver.csv')  # Should have a 'name' column

# Optionally combine with city/region if you have those columns
df['query'] = df['name']  # or df['name'] + ', ' + df['city']

# Geocode
df[['latitude', 'longitude']] = df['query'].apply(lambda x: pd.Series(geocode_place(x)))

df.to_csv('hvancouver.csv', index=False)
print("Done!")
