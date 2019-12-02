import pandas as pd
import matplotlib.pylab as plt
import re
import numpy as np
import math

#reading in KidzBopTable as pandas dataframe
dfKidzBop = pd.read_csv("KidzBopTable.csv") 

#reading in OriginalTable as pandas dataframe
dfOriginal = pd.read_csv("OriginalTable.csv")

#creating a new pandas dataframe
dfDiff = pd.DataFrame()

#create list of available metrics to access
stats = ['Popularity' , 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Loudness', 'Speechiness', 'Valence', 'Tempo', 'SwearCount', 'SentimentAverage']

sentimentDiff = np.array(list(dfOriginal["SentimentAverage"])) - np.array(list(dfKidzBop["SentimentAverage"]))
# print(sentimentDiff)

dfDiff["SentimentDifference"] = sentimentDiff

swearlessSentimentDiff = np.array(list(dfOriginal["SwearlessSentimentAverage"])) - np.array(list(dfKidzBop["SentimentAverage"]))
# print(swearlessSentimentDiff)

dfDiff["SwearlessSentimentDifference"] = swearlessSentimentDiff

#determines which words are different from one set of lyrics to the next
def compareLyrics(lyrics1, lyrics2):
    wordsList1 = np.array(lyrics1.lower().split())
    wordsList2 = np.array(lyrics2.lower().split())
    # what words are in lyrics 1, but not lyrics 2
    lyricsDiff = np.setdiff1d(wordsList1,wordsList2)
    return lyricsDiff

#make a list containing differences of stats for songs
def makeDif(stat):
#stat: the metric by which you would like to compare (str)
#from the set {Popularity ,Acousticness ,Danceability ,Energy ,Instrumentalness ,Liveness ,Loudness ,Speechiness, /
#Valence, Tempo, SwearCount, SentimentAverage}
    difList = list(map(getDif, dfOriginal[stat], dfKidzBop[stat]))
    return difList


def getDif(stat1, stat2):
    return math.fabs(stat1-stat2)


#kidzBopLyricsDiff = list(map(compareLyrics, dfKidzBop["Lyrics"].split(), dfOriginal["Lyrics"].split()))
originalLyricsDiff = list(map(compareLyrics, list(dfOriginal["Lyrics"]), list(dfKidzBop["Lyrics"])))

for stat in stats:
    dfDiff['diff%s' % stat] = makeDif(stat)

dfDiff['diffWords'] = originalLyricsDiff

#print(kidzBopLyricsDiff[0])
#print(originalLyricsDiff[0])

# saving dataframe of differences to .csv
dfDiff.to_csv('DifferenceTable.csv', index=False)
