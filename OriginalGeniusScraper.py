import requests as re
import lyricsgenius as lg
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 

#reading in KidzBopTable as pandas dataframe
dfKidzBop = pd.read_csv("KidzBopTable.csv") 

#accessing Genius API (thank you johnwmillr!)
login_token = "tAZ1oU_T0GXCZmxobxkvY0YJDSj3Kj5Tm7_Ta_LnnNJ4-35MYKi21hBeTJPUtC6U"
genius = lg.Genius(login_token)
genius.remove_section_headers = True

#accessing Spotify API
client_id = "cd3c3b7e630f47d7b588b114a877e95e"
client_secret = "40f77d47dab14786a80bd860b35ad4a8"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 

#creating a new pandas dataframe
df = pd.DataFrame(columns=['Title', 'Artist', 'Lyrics'])

#looping through the Kidz Bop dataframe
for row in dfKidzBop.itertuples(index=True, name='Pandas'):
    songKidzBop = getattr(row, "Title")
    #searching for the original artist using the Spotify API
    try:
        artistOriginal = sp.search(q = songKidzBop, type = 'track')['tracks']['items'][0]['artists'][0]['name']
        #finding the original song in genius
        songOriginal = genius.search_song(songKidzBop, artistOriginal)
    except:
        print("Song not matched")
        continue
    #adding the original song to the dataframe
    try:
        df = df.append(dict(zip(df.columns, [songOriginal.title, songOriginal.artist, songOriginal.lyrics])), ignore_index=True)
    except:
        print('Song not found in Genius')

#storing the original song dataframe as a .csv file 
df.to_csv('OriginalTable.csv')

# sp.search(q = songKidzBop, type = 'track')['tracks']['items'][0]['popularity']