import pandas as pd
import matplotlib.pyplot as plt
import wordcloud
from ast import literal_eval
import numpy as np

#load tables into pandas df
diffs = pd.read_csv("DifferenceTable.csv")
kb = pd.read_csv("KidzBopTable.csv")
original = pd.read_csv('OriginalTable.csv')

#create first plot
plt.figure(1)
#first plot: popularity of kidzbop versus original
kbPop = kb['Popularity']
orPop = original['Popularity']

plt.subplot(1,2,1)
plt.hist(kbPop, density=True, color='red', label='Kidz Bop')
plt.title("Kidz Bop Popularity")

plt.subplot(1,2,2)
plt.hist(orPop, density=True, label='Original')
plt.title("Original Popularity")
plt.subplots_adjust(wspace=.5)
plt.show()

#second plot: Difference in sentiment 
plt.figure(2)
kbSent = kb['SentimentAverage'] * 100
orSent = original['SentimentAverage'] * 100
orSentSwear = original['SwearlessSentimentAverage'] * 100
diffSent = diffs['DiffSentimentAverage'] * 100
diffSentSwearless = diffs['DiffSwearlessSentimentAverage'] * 100

plt.subplot(1,2,1)
plt.hist(kbSent, alpha=0.5, density=True, color='red', label='KidzBop')
plt.hist(orSent, alpha=0.5, density=True, label='Original')
plt.legend(loc='upper left')
plt.title("Average Sentiment Distributions")

plt.subplot(1,2,2)
plt.hist(diffSent, alpha=0.5, density=True, color='coral', label='Includes Swears')
plt.hist(diffSentSwearless, alpha=0.5, density=True, color='green', label='Swearless')
plt.title('Distribution of Sentiment Differences')
plt.legend(loc='upper left')
plt.subplots_adjust(wspace=.5)
plt.show()

#plot 3: word cloud of words removed vs words used to replace
plt.figure(3)

#take all words which have been removed from the explicit texts and add them to removed
wordsRemoved = list(map(lambda stringy: literal_eval(stringy), list(diffs["WordsRemoved"])))
removedList = [wordRemoved for index, wordRemoved in enumerate(wordsRemoved) if list(diffs["DiffWordsAverage"])[index] < 30]
removed = " ".join(np.concatenate(removedList)) 


#take all words which replaced explicit text and add to added
wordsAdded = list(map(lambda stringy: literal_eval(stringy), list(diffs["WordsAdded"])))
addedList = [wordAdded for index, wordAdded in enumerate(wordsAdded) if list(diffs["DiffWordsAverage"])[index] < 30]
added = " ".join(np.concatenate(addedList)) 

#create wordcloud objects
removedWC = wordcloud.WordCloud(max_font_size=40).generate(removed)
addedWC = wordcloud.WordCloud(max_font_size=40).generate(added)

#plot wordclouds
plt.subplot(1,2,1)
plt.imshow(removedWC, interpolation='bilinear')
plt.title("Words Removed from Explicit Lyrics")

plt.subplot(1,2,2)
plt.imshow(addedWC, interpolation='bilinear')
plt.title("Words Used to Replace Explicit Lyrics")
plt.show()

 
plt.figure(4, figsize=(12, 7))
#plot 4: show differences in song qualities
for i, word in enumerate(['Acousticness','Danceability','Energy','Instrumentalness','Liveness','Loudness','Speechiness','Valence','Tempo']):
    plt.subplot(9,1,i+1)
    plt.plot(kb[word], 'r', alpha=.5, label='KidzBop')
    plt.plot(original[word], 'b', alpha=.5, label='Original')
    if i == 0:
        plt.legend(loc='upper right') 
    plt.title(word)
plt.subplots_adjust(hspace=1.2)
plt.show()


#plot 5: distribution of genre popularity over time
plt.figure(5)

genres = list(map(lambda stringy: literal_eval(stringy), list(original["Genres"])))
print(genres)


