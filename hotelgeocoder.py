import pandas as pd
import requests
import time

API_KEY = 'AIzaSyDOAbdn-iEKjkwkXiqWubZ1hZze0gioRog'

def geocode_place(query):
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'address': query, 'key': API_KEY}
    response = requests.get(base_url, params=params).json()

    if response['status'] == 'OK':
        loc = response['results'][0]['geometry']['location']
        return loc['lat'], loc['lng']
    else:
        print(f"⚠️ Failed to geocode: {query} ({response['status']})")
        return None, None

# Load your file (adjust encoding if needed)
df = pd.read_csv('mapfile.csv', encoding='windows-1252')

# Strip whitespace and combine name and city
df['name'] = df['name'].astype(str).str.strip()
df['city'] = df['city'].astype(str).str.strip()
df['query'] = df['name'] + ', ' + df['city']

# Geocode each row with throttling
latitudes = []
longitudes = []

for query in df['query']:
    lat, lng = geocode_place(query)
    latitudes.append(lat)
    longitudes.append(lng)
    time.sleep(0.5)  # To avoid hitting rate limits (adjust as needed)

df['latitude'] = latitudes
df['longitude'] = longitudes

# Export result to JSON
df.to_json('mapfile.json', orient='records', indent=2, force_ascii=False)
print("✅ Geocoding complete. Saved to mapfile.json.")