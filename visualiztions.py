import pandas as pd
import matplotlib.pyplot as plt

#load tables into pandas df
diffs = pd.read_csv("SortedDiffs.csv")
kb = pd.read_csv("KidzBopTable.csv")
original = pd.read_csv('OriginalTable.csv')

#create first plot
plt.figure(1)
#first plot: popularity of kidzbop versus original
kbPop = kb['Popularity']
orPop = original['Popularity']

plt.subplot(1,2,1)
plt.hist(kbPop, density=True, color='red')
plt.title("Kidz Bop Popularity")

plt.subplot(1,2,2)
plt.hist(orPop, density=True)
plt.title("Original Popularity")
plt.subplots_adjust(wspace=.5)
plt.show()

#second plot: Difference in sentiment 
plt.figure(2)
kbSent = kb['SentimentAverage'] * 100
orSent = original['SentimentAverage'] * 100
orSentSwear = original['SwearlessSentimentAverage'] * 100
diffSent = diffs['DiffSentimentAverage'] * 100

plt.subplot(1,3,1)
plt.hist(kbSent, alpha=0.5, density=True, color='red')
plt.hist(orSent, alpha=0.5, density=True)
plt.legend(loc='upper left')
plt.title("Average Sentiment Distributions")
plt.show()
