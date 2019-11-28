import requests as re
import lyricsgenius as lg
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 

#accessing Genius API (thank you johnwmillr!)
login_token = "tAZ1oU_T0GXCZmxobxkvY0YJDSj3Kj5Tm7_Ta_LnnNJ4-35MYKi21hBeTJPUtC6U"
genius = lg.Genius(login_token)

#accessing Spotify API
client_id = "cd3c3b7e630f47d7b588b114a877e95e"
client_secret = "40f77d47dab14786a80bd860b35ad4a8"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 

#creating a lyricsgenius.Artist object and scraping all 684 songs from the Kidz Bop page
kidzbop = genius.search_artist("Kidz Bop", max_songs=684, sort='title', get_full_info=False)

#creating a pandas dataframe
df = pd.DataFrame(columns=['Title', 'Artist', 'Lyrics', 'SpotifyID'])

#storing info from each song in the dataframe
for song in kidzbop.songs:
    try:
        spotifyID = sp.search(q = ("artist:Kidz Bop Kids track:" + song.title), type = 'track')['tracks']['items'][0]['id']
    except: 
        print("Spotify ID for" + song.title + "not found.")
        spotifyID = ""
    df = df.append(dict(zip(df.columns, [song.title, song.artist, song.lyrics, spotifyID])), ignore_index=True) 

#storing the dataframe as a .csv file 
df.to_csv('KidzBopTable.csv')