import requests as re
import lyricsgenius as lg
import pandas as pd

#accessing Genius API (thank you johnwmillr!)
login_token = "tAZ1oU_T0GXCZmxobxkvY0YJDSj3Kj5Tm7_Ta_LnnNJ4-35MYKi21hBeTJPUtC6U"
genius = lg.Genius(login_token)
genius.remove_section_headers = True

#creating a lyricsgenius.Artist object and scraping all 684 songs from the Kidz Bop page
kidzbop = genius.search_artist("Kidz Bop", max_songs=648, sort='title', get_full_info=False)

#creating a pandas dataframe
df = pd.DataFrame(columns=['Title', 'Artist', 'Lyrics'])

#storing info from each song in the dataframe
for song in kidzbop.songs:
    df = df.append(dict(zip(df.columns, [song.title, song.artist, song.lyrics])), ignore_index=True) 

#storing the dataframe as a .csv file 
df.to_csv('KidzBopTable.csv')