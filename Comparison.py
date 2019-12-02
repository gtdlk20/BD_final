import pandas as pd
import matplotlib.pylab as plt
import re
import numpy as np

#reading in KidzBopTable as pandas dataframe
dfKidzBop = pd.read_csv("KidzBopTable.csv") 

#reading in OriginalTable as pandas dataframe
dfOriginal = pd.read_csv("OriginalTable.csv")

#creating a new pandas dataframe
df = pd.DataFrame(columns=['SentimentDifference'])

sentimentDiff = np.array(list(dfOriginal["SentimentAverage"])) - np.array(list(dfKidzBop["SentimentAverage"]))
print(sentimentDiff)

dfDiff["SentimentDifference"] = sentimentDiff