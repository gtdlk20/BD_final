import requests as re
import lyricsgenius as lg
import pandas as pd
import os

login_token = "tAZ1oU_T0GXCZmxobxkvY0YJDSj3Kj5Tm7_Ta_LnnNJ4-35MYKi21hBeTJPUtC6U"

#Create lyricsgenius scraper object (thank you johnwmillr!)
genius = lg.Genius(login_token)
genius.remove_section_headers = True

#Create a lyricsgenius.Artist object and scrapes all 684 songs from the Kidz Bop page
#stores them as lyricsgenius.Song objects, with the lyrics kept as strings
kidzbop = genius.search_artist("Kidz Bop", max_songs=648, sort='title', get_full_info=False)

df = pd.DataFrame(columns=['Title', 'Artist', 'Lyrics'])

for song in kidzbop.songs:
    df.append(pd.DataFrame(data = [song.title, song.artist, song.lyrics], columns = ['Title', 'Artist', 'Lyrics']))
  
# print dataframe. 
df.to_csv('KidzBopTable', sep='\t', encoding='utf-8')