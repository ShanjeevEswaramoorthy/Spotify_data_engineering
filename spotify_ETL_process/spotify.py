import csv

from spotipy import SpotifyClientCredentials
import spotipy
import pandas as pd
import re

# setting up the Spotify client using spotipy

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='2de01f8fdf4f4769a564e87d9504e168',
    client_secret='8dc448feeba84d5c9d65b260f62af6a8'
))

# Spotify track api url
track_endpoint = 'https://open.spotify.com/track/2sT0eosuhBEkw8dz6qFxUo'

# extracting track id from the api
track_id = re.search(r'track/([A-Za-z0-9]+)', track_endpoint).group(1)

# fetching the data based on the [track_id]
fetchTrack = sp.track(track_id)

# Extract data and store it in map
track_data = {
    'Track Name': fetchTrack['name'],
    'Artist': fetchTrack['artists'][0]['name'],
    'Album': fetchTrack['album']['name'],
    'Popularity': fetchTrack['popularity'],
    'Duration (minutes)': fetchTrack['duration_ms'] / 60000
}

# converting data into dataframe using pandas plugin
track_dataframe = pd.DataFrame([track_data])

print(track_dataframe)

# store dataframe to csv file
"""
track_dataframe.to_csv('spotify_data.csv', index=False)
"""

#  to read a csv file
"""
with open('spotify_data.csv', 'r') as file:
    read = csv.reader(file)
    for table in read:
        print(table)
"""

# to write in csv file
""""
data = [
    ['Name', 'Age', 'City'],
    ['Alice', 25, 'New York'],
    ['Bob', 30, 'Los Angeles'],
    ['Charlie', 35, 'Chicago']
]
"""
# [newline] which is used to prevent the extra spacing while writting in csv file
# no need to close the file, [with open]-> will automatically close the file
"""
with open('spotify_data.csv', 'w', newline='') as file:
    write = csv.writer(file)
    write.writerows(data)
"""


