import pandas as pd
import matplotlib.pylab as plt
import re
import numpy as np
import math
from afinn import Afinn
    
af = Afinn()

#reading in KidzBopTable as pandas dataframe
dfKidzBop = pd.read_csv("KidzBopTable.csv") 

#reading in OriginalTable as pandas dataframe
dfOriginal = pd.read_csv("OriginalTable.csv")

#creating a new pandas dataframe
dfDiff = pd.DataFrame()
dfDiff['Title'] = list(dfOriginal['Title'])

# determines which words are different from one set of lyrics to the next
def compareLyrics(lyrics1, lyrics2):
    #removes section headers and punctuation from lyrics
    lyrics1 = re.sub("[\(\[].*?[\)\]]|[^a-zA-Z0-9\s]", "", lyrics1)
    lyrics2 = re.sub("[\(\[].*?[\)\]]|[^a-zA-Z0-9\s]", "", lyrics2)
    wordsList1 = np.array(lyrics1.lower().split())
    wordsList2 = np.array(lyrics2.lower().split())
    # what words are in lyrics 1, but not lyrics 2
    lyricsDiff = np.setdiff1d(wordsList1,wordsList2)
    return lyricsDiff

originalLyricsDiff = list(map(compareLyrics, list(dfOriginal["Lyrics"]), list(dfKidzBop["Lyrics"])))
kidzBopLyricsDiff = list(map(compareLyrics, list(dfKidzBop["Lyrics"]), list(dfOriginal["Lyrics"])))

# filters word differences using sentiment score
wordRemoved = list(map(lambda wordList: [word for word in wordList if af.score(word) < 0], originalLyricsDiff))
wordsAdded = list(map(lambda wordList: [word for word in wordList if af.score(word) > 0], kidzBopLyricsDiff))

# averages the word differences between a Kidz Bop song and its original
diffWordsAverage = list(map(lambda wordList1, wordList2: (len(wordList1) + len(wordList2))/2, originalLyricsDiff, kidzBopLyricsDiff))

dfDiff['WordsRemoved'] = wordRemoved
dfDiff['WordsAdded'] = wordsAdded
dfDiff['DiffWordsAverage'] = diffWordsAverage

#create list of available metrics to access
stats = ['Popularity' , 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Loudness', 'Speechiness', 'Valence', 'Tempo', 'SwearCount', 'SentimentAverage']

#make a list containing differences of stats for songs
#from the set stats
def makeDiff(column1, column2):
    diffList = np.array(column1) - np.array(column2)
    return diffList

for stat in stats:
    dfDiff['Diff%s' % stat] = makeDiff(list(dfOriginal[stat]), list(dfKidzBop[stat]))

dfDiff['DiffSwearlessSentimentAverage'] = makeDiff(list(dfOriginal['SwearlessSentimentAverage']), list(dfKidzBop['SentimentAverage']))

# saving dataframe of differences to .csv
dfDiff.to_csv('DifferenceTable.csv', index=False)
