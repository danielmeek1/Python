#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import collections
import csv


# In[2]:


#Different Types Of Tweets
#Source:https://help.twitter.com/en/using-twitter/types-of-tweets
#1-Mentions
#2-Replies
#3-General Tweets
#4-Retweets


# In[3]:


#Reads in the refined data to perform data analysis
pd.set_option('max_colwidth', 400)
df = pd.read_csv('./data/CleanedCometLanding.csv')


# In[4]:


''' This function returns the number of mention tweets'''
def getNumberOfMentionTweets(df): 
    counter = 0
    textColumn = df['text']
    
    for (columnName, columnData) in textColumn.iteritems():

        match = re.search('RT @' , str(columnData))
        
        if match == None:
            match = re.search('@' , str(columnData))
            if match != None:
                counter = counter + 1
                    
    return counter


# In[5]:


#https://www.geeksforgeeks.org/loop-or-iterate-over-all-or-certain-columns-of-a-dataframe-in-python-pandas/
''' This function returns the number of retweets'''
def getNumberOfRetweets(df):
    counter = 0;
    textColumn = df['text']
    
    for (columnName, columnData) in textColumn.iteritems():

        match = re.search('RT @' , str(columnData))
        
        if match != None:
            counter = counter + 1
            
    return counter    
        


# In[6]:


''' This function returns the number of reply tweets '''

#Source:https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
def getNumberOfReplies(df):
     
    replies = df["in_reply_to_user_id_str"].notnull().sum()  
    
    return replies
    


# In[7]:


''' This function returns the number of general tweets'''
def getNumberOfGeneralTweets(df):
    mentions = getNumberOfMentionTweets(df)
    retweets = getNumberOfRetweets(df)
    replies = getNumberOfReplies(df)
    
    NumberOfGeneralTweets = len(df) - retweets - mentions - replies 
    return  NumberOfGeneralTweets


# In[8]:


''' This function returns total number of tweets'''
def getTotalNumberOfTweets(df):
    return len(df)


# In[9]:


''' This function returns the number of different users in the dataset'''
def getNumberOfDifferentUsers(df):
    differentUsers = df['from_user'].unique()
    return len(differentUsers)


# In[10]:


''' This function analyses the basic user behaviour''' 
''' The function prints the average number of tweets, replies, mentions, and retweets sent by a user '''
def basicUserInteractionAnalysis(df):
    differentUsers = getNumberOfDifferentUsers(df)
    averageGeneralTweetsPerUser = getNumberOfGeneralTweets(df) / differentUsers
    averageMentionsPerUser = getNumberOfMentionTweets(df) / differentUsers
    averageRetweetsPerUser = getNumberOfRetweets(df) / differentUsers
    averageRepliesPerUser = getNumberOfReplies(df) / differentUsers
    
    print("The average number of general tweets per user is:", averageGeneralTweetsPerUser)
    print("The average number of mentions tweets per user is:", averageMentionsPerUser)
    print("The average number of retweets per user is:", averageRetweetsPerUser)
    print("The average number of replies per user is:", averageRepliesPerUser)
    


# In[11]:


''' This function prints the 5 most populat hashtag in the dataset''' 
''' This function also saves all hashtags to another file for visualisation''' 
def getMostPopularHashtags(df):
    hashtags = [] 
    textColumn = df['text']
    mentionPattern = '@([a-zA-Z]+)'
    
    for (columnName, columnData) in textColumn.iteritems():  
        matchList = re.findall(mentionPattern , str(columnData))
        hashtags.extend(matchList)
    
    counter = collections.Counter(hashtags)
    
    newDataFrame = pd.DataFrame(hashtags)
    newDataFrame.to_csv('./data/Hashtags.csv',index = False)        
    
    return counter.most_common(5)


# In[12]:


''' This function prints the 5 most popular hashtag in the dataset'''
''' On top of the function above, it ensures the hashtags contain different contextual data'''
def getMostPopularCaseInsensitiveHashtags(df):
    hashtags = [] 
    textColumn = df['text']
    textColumn = textColumn.str.lower()
    mentionPattern = r'@([a-zA-Z]+)'
    
    for (columnName, columnData) in textColumn.iteritems():  
        matchList = re.findall(mentionPattern , str(columnData))
        hashtags.extend(matchList)
    
        
    counter = collections.Counter(hashtags)
    
    newDataFrame = pd.DataFrame(hashtags)
    newDataFrame.to_csv('./data/HashtagsCI.csv',index = False)    
    
    return counter.most_common(5)
            


# In[13]:


''' This function '''
# Each time data is in user's local time, adjusting time data 
# to reference data from a single point of source(such as GMT) is not
# possible for this practical since timezones were not provided in the given CSV file

def getTweetDataAboutTime(df):
    hoursList = []
    days = []
    dates = []
    createdAtColumn = df['created_at']
    timeColumn = df['time']
    
    patternForHours = r'([01]\d|2[0-3]):([0-5]\d):([0-5]\d)'
    patternForDays = r'^Mon|Tue|Wed|Thu|Fri|Sat|Sun$'
    patternForDates = r'(3[01]|[12][0-9]|0[1-9])/(1[0-2]|0[1-9])/([0-9]{4})'
    
    
    for (columnName, columnData) in createdAtColumn.iteritems():  
        hoursList_tuple = re.findall(patternForHours , str(columnData))
        daysList  = re.findall(patternForDays, str(columnData ))
        days.extend(daysList)
        hoursList.extend(hoursList_tuple)
    
    
    hours = [x[0] for x in hoursList]
      
    for (columnName, columnData) in timeColumn.iteritems():  
        dateList = re.findall(patternForDates , str(columnData))
        dates.extend(dateList)
       
        
    counterHours = collections.Counter(hours)
    counterDays = collections.Counter(days)
    counterDates = collections.Counter(dates)
    
    newDataFrame = pd.DataFrame(counterHours.most_common(5))
    newDataFrame.to_csv('./data/Hours.csv',index = False, header=False) 
    
    newDataFrame = pd.DataFrame(counterDays.most_common(5))
    newDataFrame.to_csv('./data/Days.csv',index = False , header=False)
    
    newDataFrame = pd.DataFrame(counterDates.most_common(5))
    newDataFrame.to_csv('./data/Date.csv',index = False , header=False)
    


# In[14]:


#''' Replacement for switch case statement is to use a dictionary mapping'''
#def applicationParser(argument):
#    switcher = {
#        'Twitter Web Client' : 'Mobile Browser',
#        'Twitter for Websites': 'Browser',
#        'Twitter for iPad' : 'iPad App',
#        'Twitter for iPhone' : 'iPhone App' ,
#        'Twitter for Android': 'Android App',
#        'Twitter for BlackBerryÂ®': 'BlackBerry App'
#    }

#    return switcher.get(argument, "nothing")


# In[15]:


''' This function returns the most popular 5 app used to send the tweets'''
''' This function also returns a seperate file with all the apps used for visualisation'''

def getMostPopularApplicationsUsed(df):
    applications = [] 
    whichApplicationColumn = df['source']
    
    patternForApplications = r'(?<=>).*(?=<)'
    
    for (columnName, columnData) in whichApplicationColumn.iteritems():

        matchList = re.findall(patternForApplications, str(columnData))
        applications.extend(matchList)
    
    counterApplications = collections.Counter(applications)
    
    newDataFrame = pd.DataFrame(counterApplications.most_common(5))
    newDataFrame.to_csv('./data/applications.csv',index = False, header=False) 

    
    return counterApplications.most_common(5)
    
    


# In[16]:


def performDataAnalysis(df):
    print ('The number of mention tweets is' , getNumberOfMentionTweets(df))
    print ('The number of retweets is' , getNumberOfRetweets(df))
    print ('The number of reply tweets is' , getNumberOfReplies(df))
    print ('The number of general tweets is' , getNumberOfGeneralTweets(df))
    print ('The number of total number of tweets is' , getTotalNumberOfTweets(df))
    print ('The number of different users is' , getNumberOfDifferentUsers(df))
    basicUserInteractionAnalysis(df)
    print('5 most popular hashtags with their respective occurances are',getMostPopularHashtags(df))
    print('5 contextually different most popular hashtags with their respective occurances are' 
          ,getMostPopularCaseInsensitiveHashtags(df))
    getTweetDataAboutTime(df)
    print('5 most popular apps to send tweets are', getMostPopularApplicationsUsed(df))


# In[17]:


performDataAnalysis(df)


# In[ ]:




