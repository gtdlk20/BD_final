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

print(filthOriginal)

#gets the average sentiment of a songs words
def getAverageSentiment(lyrics):
    # wordList is a list of words devoid of stopwords, numbers, and punctuation. 
    wordList = [word for word in re.sub("[^a-zA-Z\s]", '', lyrics).lower().split() if word not in stopwords]
    # calculates the average sentiment by summing up the sentiment score for each word then dividing it by the length of the wordList
    averageSentiment = sum(list(map(af.score, wordList))) / len(wordList)
    return averageSentiment

# creates a list containing the average sentiment scores of every song. 
averageSentimentKidzBop = list(map(getAverageSentiment, list(dfKidzBop["Lyrics"])))
averageSentimentOriginal = list(map(getAverageSentiment, list(dfOriginal["Lyrics"])))

print(averageSentimentKidzBop)

# #return plot of sent scores
def get_song_sent_graph(title, lyrics):
    lyrics = lyrics.split()
    scores = [get_sentiment_score(word) for word in lyrics]
    index = range(lyrics)
    plt.plot(index, scores, 'r+')
    plt.title('Sentiment score by word of %s' % title)
    plt.show()

# #returns histogram of sentiment scores
def get_sent_hist(scores, header):
    #param scores: list of tuples containing song names and sentiment scores
    #param hesder: title of plot
    plt.hist([score[1] for score in scores])
    plt.title(header)
    plt.show()

# #get sentiment scores for each kidzbop and original song
kidzbop_sent_scores = get_df_sent_scores(dfKidzBop)
original_sent_scores = get_df_sent_scores(dfOriginal)

get_sent_hist(kidzbop_sent_scores, "KidzBop sentiment scores")