import pandas as pd
import nltk
nltk.download('stopwords')
from afinn import Afinn
import matplotlib.pylab as plt

# Get a list of stopwords from nltk
stopwords = nltk.corpus.stopwords.words("english")

#reading in KidzBopTable as pandas dataframe
dfKidzBop = pd.read_csv("KidzBopTable.csv") 

#reading in OriginalTable as pandas dataframe
dfOriginal = pd.read_csv("OriginalTable.csv")

#create new Afinn object for sentiment analysis
af = Afinn()

# YOU CAN USE INDEXING FUNCTIONS TO MAKE THIS RUN FASTER INSTEAD OF CREATING YOUR OWN METHOD WITH A FOR LOOP !!!!!!!!!!!!!!:
# https://www.geeksforgeeks.org/python-count-of-elements-matching-particular-condition/ 
# I like method 2 personally. your condition can be if the value is in swears[] !!!!!!!!!!!!!!!!!!!
#returns number of basic swear words found in song lyrics
def count_swears(lyrics):
#param lyrics: a string of song lyrics

    swears = ['ass', 'shit', 'fuck', 'bitch', 'cunt', 'hell', 'nigga']
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

# IF YOU ARE RETURNING A LIST THE SAME SIZE AS THE INPUT USE MAP!!!!!!!!!!!!!!!!!!!!!!!!!!
# https://www.geeksforgeeks.org/python-map-function/
# IT IS MUCH MUCH FASTER THAN A SEPARATE METHOD WITH A FOR LOOP!!!!!!!!!
# map(list(dfKidzBop["Lyrics"]), get_basic)filthiness) should return a list the same size as the titles column with the filth scores
#returns list of tuples (title, filth) where filth is the filth score of a song
def get_df_filth(df):
    #param df: a pandas dataframe
    filth = []
    for row in df.itertuples(index=True, name='Pandas'):
        title = getattr(row, 'Title')
        lyrics = getattr(row, 'Lyrics')
        filth.append((title, get_basic_filthiness(lyrics)))
    return filth

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
    # USE REGULAR EXPRESSIONS TO REMOVE THESE!!!!!!!!!!!!!!!!!!!!
    # re.sub([a-zA-Z0-9\s], '', word) for example will remove everything that not a letter, digit, or space
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
    # You can just do a regular expression for this!!!!!!!!!!!!!!!!!!!!!!!!!!
    # re.sub([a-zA-Z\s], '', word) for example will remove anything thats not a letter or space
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
    words = filter_lyrics(lyrics)
    
    for word in words:
        #add the sentiment score of each word to score
        for word in words:
            score += af.score(word)

    #return the average sentiment score over all evaluated words
    return score / len(words)

# AGAIN LOOK INTO USING MAP FOR THIS
#return list of tuples (title, sent_score) for dataframe
def get_df_sent_scores(df):
    sent = []
    for row in df.itertuples(index=True, name='Pandas'):
        title = getattr(row, 'Title')
        lyrics = getattr(row, 'Lyrics')
        sent.append((title, get_lyrics_sentiment_score(lyrics)))
    return sent

#get filth scores of kidz bop- presumably zero
kbFilth = get_df_filth(dfKidzBop)
#get filth scores of original songs
originalFilth = get_df_filth(dfOriginal)

#return plot of sent scores
def get_song_sent_graph(title, lyrics):
    lyrics = lyrics.split()
    scores = [get_sentiment_score(word) for word in lyrics]
    index = range(lyrics)
    plt.plot(index, scores, 'r+')
    plt.title('Sentiment score by word of %s' % title)
    plt.show()

#returns histogram of sentiment scores
def get_sent_hist(scores, header):
    #param scores: list of tuples containing song names and sentiment scores
    #param hesder: title of plot
    plt.hist([score[1] for score in scores])
    plt.title(header)
    plt.show()

#get sentiment scores for each kidzbop and original song
kidzbop_sent_scores = get_df_sent_scores(dfKidzBop)
#original_sent_scores = get_df_sent_scores(dfOriginal)

get_sent_hist(kidzbop_sent_scores, "KidzBop sentiment scores")