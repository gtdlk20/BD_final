import requests as re
import lyricsgenius as lg
login_token = "tAZ1oU_T0GXCZmxobxkvY0YJDSj3Kj5Tm7_Ta_LnnNJ4-35MYKi21hBeTJPUtC6U"

#Create lyricsgenius scraper object (thank you johnwmillr!)
genius = lg.Genius(login_token)
genius.remove_section_headers = True

#Create a lyricsgenius.Artist object and scrapes all 684 songs from the Kidz Bop page
#stores them as lyricsgenius.Song objects, with the lyrics kept as strings
kidzbop = genius.search_artist("Kidz Bop", max_songs=648, sort='title', get_full_info=False)

def get_artist_word_count(artist):
    """param artist: lyricsgenius.Artist object
       returns number of words in an artists library
    """
    if artist.num_songs == 0:
        return 0
    else:
        total_wc = 0
        for song in artist.songs:
            #clear all escape chars and make a list of lyrics
            lyrics_list = song.lyrics.split()
            #sum lengths
            total_wc += len(lyrics_list)
        return total_wc
        
print(get_artist_word_count(kidzbop))


kb_lyrics = open('kidzbop.txt', 'w+')

for song in kidzbop.songs:
    kb_lyrics.write(song.lyrics)

kb_lyrics.close()