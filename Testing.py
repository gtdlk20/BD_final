import re
import lyricsgenius as lg
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import numpy as np
import Levenshtein as lev
import profanity_check

#accessing Genius API (thank you johnwmillr!)
login_token = "tAZ1oU_T0GXCZmxobxkvY0YJDSj3Kj5Tm7_Ta_LnnNJ4-35MYKi21hBeTJPUtC6U"
genius = lg.Genius(login_token)

#accessing Spotify API
client_id = "cd3c3b7e630f47d7b588b114a877e95e"
client_secret = "40f77d47dab14786a80bd860b35ad4a8"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 

# song = sp.search(q = "Old Town Road", type = 'track')['tracks']['items']

# print(len(song))

# code below won't not include kidz bop songs for some reason
# scrapes = sp.search(q = re.sub("[^a-zA-Z0-9\s]", '', "Club Can't Handle Me"), type = 'track')['tracks']['items']
# titleMatches = [scrape['name'] for scrape in scrapes if scrape['artist'][0]['name'] != "Kidz Bop Kids"]
# indexMatch = np.argmin(np.array([lev.distance(titleMatch, "Club Can't Handle Me") for titleMatch in titleMatches])) 
# SpotifyID = scrapes[indexMatch]['id']

# print(titleMatches)
# print(indexMatch)

# Spotify id 
# SpotifyID = song[0]['id']

# song info fron get a track 
# print(sp.track(SpotifyID)['name'])
# print(sp.track(SpotifyID)['artists'][0]['name'])
# print(sp.track(SpotifyID)['popularity'])
# print(sp.track(SpotifyID)['album']['name'])

# song audio info from get audio features
# print(sp.audio_features(SpotifyID)[0]['danceability'])

# print(genius.search_song('kidzBopSong', 'originalArtist'))

# print(re.sub("[^a-zA-Z0-9\s]", '', "1 Thing"))

# song = genius.search_song("All You Need Is Love - 2009 Remaster", 'The Beatles')
# print(song.lyrics)

# song = genius.search_song("All You Need Is Love    ", 'The Beatles')
# print(song.lyrics)


# title = 'Ain\'t no thank - da police'
# print(re.sub('\([^)]*\)|-.*|[^a-zA-Z0-9\s]', '', title))