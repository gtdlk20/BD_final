import pandas as pd
import matplotlib.pyplot as plt

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



