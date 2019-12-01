import pandas as pd
import nltk
# nltk.download('stopwords')
from afinn import Afinn
import matplotlib.pylab as plt
import profanity_check
import re

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