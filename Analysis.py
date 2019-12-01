import pandas as pd
import nltk
# nltk.download('stopwords')
from afinn import Afinn
import matplotlib.pylab as plt
import profanity_check
import re

# Get a list of stopwords from nltk
stopwords = nltk.corpus.stopwords.words("english")

#reading in KidzBopTable as pandas dataframe
dfKidzBop = pd.read_csv("KidzBopTable.csv") 

#reading in OriginalTable as pandas dataframe
dfOriginal = pd.read_csv("OriginalTable.csv")

#create new Afinn object for sentiment analysis
af = Afinn()

# creates a list containing the number of swear words in each songs lyrics
# profanity_check.predict returns a list of 1s and Os: 1 if a word is a swear word, 0 if it is not
filthKidzBop = list(map(lambda lyrics: sum(profanity_check.predict(lyrics.lower().split())), list(dfKidzBop["Lyrics"])))
filthOriginal = list(map(lambda lyrics: sum(profanity_check.predict(lyrics.lower().split())), list(dfOriginal["Lyrics"])))

# print(filthOriginal)

# appending lists to their respective dataframes
dfKidzBop["SwearCount"] = filthKidzBop
dfOriginal["SwearCount"] = filthOriginal

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
averageSentimentKidzBop = list(map(getAverageSentiment, list(dfKidzBop["Lyrics"])))
averageSentimentOriginal = list(map(getAverageSentiment, list(dfOriginal["Lyrics"])))

# print(averageSentimentKidzBop)

# appending lists to their respective dataframes
dfKidzBop["SentimentAverage"] = averageSentimentKidzBop
dfOriginal["SentimentAverage"] = averageSentimentOriginal

#storing the updated dataframes in their .csv format
dfKidzBop.to_csv('KidzBopTable.csv')
dfOriginal.to_csv('OriginalTable.csv')

