import re
import lyricsgenius as lg
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import Levenshtein as lev
import numpy as np

#reading in KidzBopTable as pandas dataframe
dfKidzBop = pd.read_csv("KidzBopTable.csv") 

#accessing Genius API (thank you johnwmillr!)
login_token = "tAZ1oU_T0GXCZmxobxkvY0YJDSj3Kj5Tm7_Ta_LnnNJ4-35MYKi21hBeTJPUtC6U"
genius = lg.Genius(login_token)

#accessing Spotify API
client_id = "cd3c3b7e630f47d7b588b114a877e95e"
client_secret = "40f77d47dab14786a80bd860b35ad4a8"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 

#creating a new pandas dataframe
df = pd.DataFrame(columns=['Title', 'Artist', 'ReleaseDate', 'Lyrics', 'Acousticness', 
'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Loudness', 'Speechiness', 'Valence', 'Tempo'])

#looping through the Kidz Bop dataframe
for row in dfKidzBop.itertuples(index=True, name='Pandas'):
    kidzBopTitle = getattr(row, "Title")
    try:
        # scraping Spotify data (original song)
        scrapes = sp.search(q = re.sub("[^a-zA-Z0-9\s]", '', kidzBopTitle), type = 'track')['tracks']['items']
        # creating a list of title matches from non Kidz Bop artists
        titleMatches = [scrape['name'] for scrape in scrapes if scrape['artists'][0]['name'] != 'Kidz Bop Kids']
        # finding the index of the closest title match
        indexMatch = np.argmin(np.array([lev.distance(titleMatch, kidzBopTitle) for titleMatch in titleMatches])) 
        # loading remaining data with the Spotify ID
        spotifyID = scrapes[indexMatch]['id']
        track = sp.track(spotifyID)
        audio_features = sp.audio_features(spotifyID)[0]
        # formatting Spotify data
        title = track['name']
        artist = track['artists'][0]['name']
        releaseDate = track['album']['release_date']
        acousticness = audio_features['acousticness']
        danceability = audio_features['danceability']
        energy = audio_features['energy']
        instrumentalness = audio_features['instrumentalness']
        liveness = audio_features['liveness']
        loudness = audio_features['loudness']
        speechiness = audio_features['speechiness']
        valence = audio_features['valence']
        tempo = audio_features['tempo']
        # scraping Genius data (original song)
        song = genius.search_song(re.sub('\([^)]*\)|-.*', '', title), re.sub('\([^)]*\)|-.*', '', artist))
        # appending to df
        df = df.append(dict(zip(df.columns, [title, artist, releaseDate, song.lyrics, 
        acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, valence, tempo])), ignore_index=True) 
    except:
        print("Match for " + kidzBopTitle + " not found.")

#storing the original song dataframe as a .csv file 
df.to_csv('OriginalTable.csv')
