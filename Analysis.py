import pandas as pd
import nltk
# nltk.download('stopwords')
from afinn import Afinn
import matplotlib.pylab as plt
import profanity_check
import re
import numpy as np

# Get a list of stopwords from nltk
stopwords = nltk.corpus.stopwords.words("english")

#reading in KidzBopTable as pandas dataframe
dfKidzBop = pd.read_csv("KidzBopTable.csv") 

#reading in OriginalTable as pandas dataframe
dfOriginal = pd.read_csv("OriginalTable.csv")

#reading in DifferenceTable as pandas dataframe

#create new Afinn object for sentiment analysis
af = Afinn()

# creates a list containing the number of swear words in each songs lyrics
# profanity_check.predict returns a list of 1s and Os: 1 if a word is a swear word, 0 if it is not
swearCountKidzBop = list(map(lambda lyrics: sum(profanity_check.predict(lyrics.lower().split())), list(dfKidzBop["Lyrics"])))
swearCountOriginal = list(map(lambda lyrics: sum(profanity_check.predict(lyrics.lower().split())), list(dfOriginal["Lyrics"])))

# appending lists to their respective dataframes
dfKidzBop["SwearCount"] = swearCountKidzBop
dfOriginal["SwearCount"] = swearCountOriginal

#gets the average sentiment of a songs words
def getAverageSentiment(lyrics):
    # wordList is a list of words devoid of stopwords, numbers, and punctuation. 
    wordList = [word for word in re.sub("[^a-zA-Z\s]", '', lyrics).lower().split() if word not in stopwords]
    # calculates the average sentiment by summing up the sentiment score for each word then dividing it by the length of the wordList
    try:
        averageSentiment = sum(list(map(af.score, wordList))) / len(wordList)
    except:
        averageSentiment = 0
    return averageSentiment

# creates a list containing the average sentiment scores of every song. 
sentimentAverageKidzBop = list(map(getAverageSentiment, list(dfKidzBop["Lyrics"])))
sentimentAverageOriginal = list(map(getAverageSentiment, list(dfOriginal["Lyrics"])))

dfKidzBop["SentimentAverage"] = sentimentAverageKidzBop
dfOriginal["SentimentAverage"] = sentimentAverageOriginal

# removes swear words from lyrics, returning a clean string
def removeSwears(lyrics):
    wordsList = np.array(lyrics.lower().split())
    swearList = np.array(profanity_check.predict(wordsList))
    wordsListCleaned = np.delete(wordsList, np.where(swearList == 1)[0])
    return " ".join(wordsListCleaned)

# creates a list containing the average sentiment scores of every song, after swear words have been removed. 
swearlessSentimentAverageOriginal = list(map(getAverageSentiment, list(map(removeSwears, list(dfOriginal["Lyrics"])))))

dfOriginal["SwearlessSentimentAverage"] = swearlessSentimentAverageOriginal

dfKidzBop["PossibleGenres"] = list(dfOriginal["Genres"])

#storing the updated dataframes in their .csv format
dfKidzBop.to_csv('KidzBopTable.csv', index=False)
dfOriginal.to_csv('OriginalTable.csv', index=False)

