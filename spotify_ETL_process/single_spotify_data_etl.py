import pandas as pd
import re
from spotipy import SpotifyClientCredentials
import spotipy
import mysql.connector
from mysql.connector import Error

# ETL - Extract Transform Load


# Extracting a data
# [step 1] Need to give the [Spotify] creditionals

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='2de01f8fdf4f4769a564e87d9504e168',
    client_secret='8dc448feeba84d5c9d65b260f62af6a8'
))

# [step 2] take the api endpoint
track_endpoint = 'https://open.spotify.com/track/02wf1NAQdIpe5S1NJYPwvB'

# [step 3] extract the track id
track_id = re.search(r'track/([A-Za-z0-9]+)', track_endpoint).group(1)

# [step 4] hit the api using [spotipy] client and store the data in [fetchTrack]
fetchTrack = sp.track(track_id)

# [step 5] store the data in dictionary object
fetchData = {
    'Track Name': fetchTrack['name'],
    'Artist': fetchTrack['artists'][0]['name'],
    'Album': fetchTrack['album']['name'],
    'Popularity': fetchTrack['popularity'],
    'Duration (minutes)': fetchTrack['duration_ms'] / 60000
}

# [Step 5] covert dictionary object into dataframe
covertDataToDataFrame = pd.DataFrame([fetchData])

try:
    # Load -> loading the data to sources such as api, database,etc.,
    # [step 6] JDBC - connecting to the server

    connection = mysql.connector.connect(
        host='localhost',
        database='spotify_demo',
        user='root',
        password='Shanjeev_root'
    )

    # [step 7] check database is connected
    if connection.is_connected():
        print('database connected Successfully')

        # [Step 8] create the cursor object which is user to interact with you sql database
        cursor = connection.cursor()

        # [Step 9] create the table in your database
        createSpotifyTable = """CREATE TABLE IF NOT EXISTS Spotify_demo_table( 
                          track_id int AUTO_INCREMENT Primary key,
                          track_name varchar(300),
                          artist varchar(100), 
                          album varchar(300),
                          popularity int,
                          duration int
                          );"""

        # [Step 10] cursor.execute -> this will create the table in you database [spotify_demo]
        cursor.execute(createSpotifyTable)

        # [Step 11] commit your changes in database
        connection.commit()

        # [Step 12] load the data to the database or source from the api
        insertQuery = """INSERT INTO Spotify_demo_table (track_name, artist, album, popularity, 
        duration) VALUES (%s, %s, %s, %s, %s)"""

        # Extracting values from fetchData
        insertValues = [(
          fetchData['Track Name'],
          fetchData['Artist'],
          fetchData['Album'],
          fetchData['Popularity'],
          int(fetchData['Duration (minutes)'] * 60)
          )]

        cursor.executemany(insertQuery, insertValues)

        connection.commit()

        print('value inserted created successfully')

        cursor.close()
        connection.close()

except Error as e:
    print('error occur while fetching ->', e)

finally:
    cursor.close()
    connection.close()

