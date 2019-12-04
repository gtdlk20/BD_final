import re
import lyricsgenius as lg
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials 
import numpy as np
import Levenshtein as lev

#accessing Genius API (thank you johnwmillr!)
login_token = "tAZ1oU_T0GXCZmxobxkvY0YJDSj3Kj5Tm7_Ta_LnnNJ4-35MYKi21hBeTJPUtC6U"
genius = lg.Genius(login_token)

#accessing Spotify API
client_id = "cd3c3b7e630f47d7b588b114a877e95e"
client_secret = "40f77d47dab14786a80bd860b35ad4a8"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) 

#reading in KidzBopTable as pandas dataframe
dfKidzBop = pd.read_csv("KidzBopTable.csv") 

#reading in OriginalTable as pandas dataframe
dfOriginal = pd.read_csv("OriginalTable.csv")

#reading in DifferenceTable as pandas dataframe
dfDiff = pd.read_csv("DifferenceTable.csv")

# print(list(dfOriginal.loc[dfOriginal['Title'] == 'Too Close', 'Lyrics']))
# print("\n Kidz Bop \n")
# print(list(dfKidzBop.loc[dfKidzBop['Title'] == 'Too Close', 'Lyrics']))

from ast import literal_eval

wordsRemoved = list(map(lambda stringy: literal_eval(stringy), list(dfDiff["WordsRemoved"])))
test = " ".join(np.concatenate(wordsRemoved)) 
print(test)