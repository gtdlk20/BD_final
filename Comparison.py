import pandas as pd
import matplotlib.pylab as plt
import re
import numpy as np

#reading in KidzBopTable as pandas dataframe
dfKidzBop = pd.read_csv("KidzBopTable.csv") 

#reading in OriginalTable as pandas dataframe
dfOriginal = pd.read_csv("OriginalTable.csv")

#creating a new pandas dataframe
dfDiff = pd.DataFrame()

sentimentDiff = np.array(list(dfOriginal["SentimentAverage"])) - np.array(list(dfKidzBop["SentimentAverage"]))
# print(sentimentDiff)

dfDiff["SentimentDifference"] = sentimentDiff

swearlessSentimentDiff = np.array(list(dfOriginal["SwearlessSentimentAverage"])) - np.array(list(dfKidzBop["SentimentAverage"]))
# print(swearlessSentimentDiff)

dfDiff["SwearlessSentimentDifference"] = swearlessSentimentDiff


def compareLyrics(lyrics1, lyrics2):
    wordsList1 = np.array(lyrics1.lower().split())
    wordsList2 = np.array(lyrics2.lower().split())
    # what words are in lyrics 1, but not lyrics 2
    lyricsDiff = np.setdiff1d(wordsList1,wordsList2)
    return lyricsDiff

kidzBopLyricsDiff = list(map(compareLyrics, list(dfKidzBop["Lyrics"]), list(dfOriginal["Lyrics"])))
originalLyricsDiff = list(map(compareLyrics, list(dfOriginal["Lyrics"]), list(dfKidzBop["Lyrics"])))

print(kidzBopLyricsDiff[0])
print(originalLyricsDiff[0])

# saving dataframe of differences to .csv
dfDiff.to_csv('DifferenceTable.csv', index=False)
