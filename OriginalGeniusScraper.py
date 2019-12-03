import re
import lyricsgenius as lg
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import Levenshtein as lev
import numpy as np

#reading in KidzBopTable as pandas dataframe
dfKidzBop = pd.read_csv("KidzBopTable.csv") 

#accessing Genius API
login_token = "tAZ1oU_T0GXCZmxobxkvY0YJDSj3Kj5Tm7_Ta_LnnNJ4-35MYKi21hBeTJPUtC6U"
genius = lg.Genius(login_token)

#accessing Spotify API
client_id = "cd3c3b7e630f47d7b588b114a877e95e"
client_secret = "40f77d47dab14786a80bd860b35ad4a8"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 

#creating a new pandas dataframe
df = pd.DataFrame(columns=['Title', 'Artist', 'ReleaseDate', 'Lyrics', 'Genres', 'Popularity', 'Acousticness', 
'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Loudness', 'Speechiness', 'Valence', 'Tempo'])

#looping through the Kidz Bop dataframe
for index, row in dfKidzBop.iterrows():
    kidzBopTitle = row['Title']
    try:
        # scraping Spotify data (original song)
        searches = sp.search(q = re.sub("[^a-zA-Z0-9\s]", '', kidzBopTitle), type = 'track')['tracks']['items']
        artists = np.array([search['artists'][0]['name'] for search in searches])
        kidzBopIndex = list(np.where(artists == 'Kidz Bop Kids')[0])
        for index in sorted(kidzBopIndex, reverse=True):
            del searches[index]

        kidzBopLyrics = row['Lyrics']
        lyricsList = np.array([genius.search_song(re.sub('\([^)]*\)|-.*', '', 
        search['name']), search['artists'][0]['name']).lyrics for search in searches])
        
        index = np.argmin(list(map(lambda lyrics: len(np.setdiff1d(kidzBopLyrics.lower().split(), 
        lyrics.lower().split())), lyricsList)))

        lyrics = lyricsList[index]
        track = sp.track(searches[index]['id'])
        artist = sp.artist(searches[index]['artists'][0]['id'])
        audio_features = sp.audio_features(searches[index]['id'])[0]

        # formatting Spotify data
        title = track['name']
        releaseDate = track['album']['release_date']
        popularity = track['popularity']
        artistName = artist['name']
        genres = artist['genres']
        acousticness = audio_features['acousticness']
        danceability = audio_features['danceability']
        energy = audio_features['energy']
        instrumentalness = audio_features['instrumentalness']
        liveness = audio_features['liveness']
        loudness = audio_features['loudness']
        speechiness = audio_features['speechiness']
        valence = audio_features['valence']
        tempo = audio_features['tempo']
        
        # appending to df
        df = df.append(dict(zip(df.columns, [kidzBopTitle, artistName, releaseDate, lyrics, genres, popularity,
        acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo])), ignore_index=True) 
    except:
        print("Complete match for " + kidzBopTitle + " not found.")
        dfKidzBop.drop(index=index, inplace=True)

#storing the original song dataframe as a .csv file 
df.to_csv('OriginalTable.csv', index=False)
# updating the Kidz Bop song dataframe
dfKidzBop.to_csv('KidzBopTable.csv', index=False)
