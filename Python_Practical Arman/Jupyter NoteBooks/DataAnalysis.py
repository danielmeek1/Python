#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import collections


# In[2]:


#Different Types Of Tweets
#Source:https://help.twitter.com/en/using-twitter/types-of-tweets
#Mentions
#Replies
#General Tweets
#.Retweets
#    A subset of retweets are called retweet with comments


# In[3]:


pd.set_option('max_colwidth', 400)
df = pd.read_csv('./data/CleanedCometLanding.csv')


# In[5]:


def getNumberOfMentionTweets(df): 
    counter = 0;
    textColumn = df['text']
    
    for (columnName, columnData) in textColumn.iteritems():

        match = re.search('RT @' , columnData)
        
        if match == None:
            match = re.search('@' , columnData)
            if match != None:
                counter = counter + 1
            
    return counter


# In[6]:


getNumberOfMentionTweets(df)


# In[7]:


#https://www.geeksforgeeks.org/loop-or-iterate-over-all-or-certain-columns-of-a-dataframe-in-python-pandas/
''' Gets the number of retweets'''
def getNumberOfRetweets(df):
    counter = 0;
    textColumn = df['text']
    
    for (columnName, columnData) in textColumn.iteritems():

        match = re.search('RT @' , columnData)
        
        if match != None:
            counter = counter + 1
            
    return counter    
        


# In[8]:


getNumberOfRetweets(df)


# In[9]:


''' Returns the number of reply tweets '''

#Source:https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
def getNumberOfReplies(df):
    
    replies = df["in_reply_to_user_id_str"].notnull().sum()  
    return replies
    #return df["in_reply_to_status_id_str"].notnull().sum()


# In[10]:


getNumberOfReplies(df)


# In[11]:


def getNumberOfGeneralTweets(df):
    mentions = getNumberOfMentionTweets(df)
    retweets = getNumberOfRetweets(df)
    replies = getNumberOfReplies(df)
    NumberOfGeneralTweets = len(df) - retweets - mentions - replies 
    return NumberOfGeneralTweets


# In[12]:


getNumberOfGeneralTweets(df)


# In[13]:


def getTotalNumberOfTweets(df):
    return len(df)


# In[14]:


getTotalNumberOfTweets(df)


# In[15]:


def getNumberOfDifferentUsers(df):
    differentUsers = df['from_user'].unique()
    return (len(differentUsers))


# In[16]:


getNumberOfDifferentUsers(df)


# In[17]:


# the average number of tweets and replies sent by users
def basicAnalysisOfData(df):
    differentUsers = getNumberOfDifferentUsers(df)
    averageGeneralTweetsPerUser = getNumberOfGeneralTweets(df) / differentUsers
    averageMentionsPerUser = getNumberOfMentionTweets(df) / differentUsers
    averageRetweetsPerUser = getNumberOfRetweets(df) / differentUsers
    averageRepliesPerUser = getNumberOfReplies(df) / differentUsers
    
    print("The average number of general tweets per user is:", averageGeneralTweetsPerUser)
    print("The average number of mentions tweets per user is:", averageMentionsPerUser)
    print("The average number of retweets per user is:", averageRetweetsPerUser)
    print("The average number of replies per user is:", averageRepliesPerUser)
    


# In[18]:


basicAnalysisOfData(df)


# In[19]:


def getMostPopularHashtags(df):
    hashtags = [] 
    textColumn = df['text']
    mentionPattern = '@([a-zA-Z]+)'
    
    for (columnName, columnData) in textColumn.iteritems():  
        matchList = re.findall(mentionPattern , columnData)
        hashtags.extend(matchList)
    
    counter = collections.Counter(hashtags)
    print(counter.most_common(5))
            


# In[20]:


getMostPopularHashtags(df)


# In[29]:


def getMostPopularCaseInsensitiveHashtags(df):
    hashtags = [] 
    textColumn = df['text']
    mentionPattern = '@([a-zA-Z]+)'
    
    for (columnName, columnData) in textColumn.iteritems():  
        matchList = re.findall(mentionPattern , columnData)
        hashtags.extend(matchList)
    
        
    counter = collections.Counter(map(str.lower,hashtags))
    print(counter.most_common(5))
            


# In[30]:


getMostPopularCaseInsensitiveHashtags(df)


# In[ ]:




