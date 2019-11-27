import pandas as pd
import nltk
nltk.download('stopwords')
from afinn import Afinn

# Get a list of stopwords from nltk
stopwords = nltk.corpus.stopwords.words("english")

#reading in KidzBopTable as pandas dataframe
dfKidzBop = pd.read_csv("KidzBopTable.csv") 

#reading in OriginalTable as pandas dataframe
dfOriginal = pd.read_csv("OriginalTable.csv")

#create new Afinn object for sentiment analysis
af = Afinn()

#returns number of basic swear words found in song lyrics
def count_swears(lyrics):
#param lyrics: a string of song lyrics

    swears = ['ass', 'shit', 'fuck', 'bitch', 'cunt', 'hell']
    song = lyrics.lower().split()
    total = 0

    for word in song:
      if word in swears:
            total += 1

    return total

#returns ratio of swears to non-swears
def get_basic_filthiness(lyrics):
    #param lyrics: a string of song lyrics
    num_swears = count_swears(lyrics)
    return num_swears / (len(lyrics.split()) - num_swears)



#preprocesses lyrics for sentiment analysis: removes all stopwords (from nltk) and numbers 
#returns list of analyzable words
def filter_lyrics(lyrics):
    
    def _isnum(w):
        try:
            int(w)
            return True
        except ValueError:
            return False

    #removes punctuation from words
    def remove_punct(word):
        punct = ['.', ',', ':', ';', '(', ')', '_', '-', '?', '!', '/', '`']
        w = ''

        for c in word:
            if not c in punct:
                w += c
        return w

    
    # Set words to lowercase and remove them if they are stop words, otherwise remove punctuation
    words = [remove_punct(w.lower()) for w in lyrics.split() if w.lower() not in stopwords]

    # Remove numbers
    words = [w for w in words if not _isnum(w)]

    return words

#returns sentiment score of word
def get_sentiment_score(word):
    #param word: a valid string
    return af.score(word)

#returns the sentiment score of a string of lyrics
def get_lyrics_sentiment_score(lyrics):
#param lyrics: a string of lyrics

    #initialize score to 0
    score = 0
    #filter lyrics of stop words, numbers, puntiation
    words = filter_words(lyrics)
    
    for word in words:
        #add the sentiment score of each word to score
        for word in words:
            score += af.score(word)

    #return the average sentiment score over all evaluated words
    return score / len(words)

