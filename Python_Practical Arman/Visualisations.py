#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.gridspec import GridSpec
import DataAnalysis as da
import numpy as np


# In[ ]:


pd.set_option('max_colwidth', 400)
df = pd.read_csv('./data/CleanedCometLanding.csv')


# In[ ]:


''' Creates a pie chart for the structure of the dataset (tweets/retweets/replies)'''

def visualiseStruct(df):
    labels = ['General tweets', 'Mentions', 'Retweets', 'Replies']
    proportions = []

    proportions.append(da.getNumberOfGeneralTweets(df))
    proportions.append(da.getNumberOfMentionTweets(df))
    proportions.append(da.getNumberOfRetweets(df))
    proportions.append(da.getNumberOfReplies(df))

   plt.pie(proportions)
   plt.show()


# In[ ]:


visualiseStruct(df)


# In[ ]:




