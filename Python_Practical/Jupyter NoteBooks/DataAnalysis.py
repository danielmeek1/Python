#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import collections
import csv


# # Data Analysis Justifications
# 
# From the beginning, we always reminded ourselves this project is a data analysis project. We wanted to have a pipeline where the data would go through to generate the end result. Therefore we seperated the project into 3 parts. Data Refinement, Data Analysis, and Data Representation(Visualisation). 
# 
# In data analysis, our goal is to extract the knowledge and feed it to the next pipeline which is visualisation. While we do print the results of our data analysis which can be argued to be the data representation part, we believe this is necessary due to the relatively simple nature of this practical in the world of data science. We believe in real life applications, the knowledge would often require more delivery methods to aid learning such as graphs.
# 
# This is the reasoning why we save most of the data to seperate csv files which then can be utilized by the visualisation module.
# 
# Once again, we have utilized the twitter API to utilize the data better.
# We identified 4 different types of tweets these are:
# 
# Source:https://help.twitter.com/en/using-twitter/types-of-tweets
# 1-Mentions
# 2-Replies
# 3-General Tweets
# 4-Retweets
# 
# While the practical specification only requires tweets, retweets, and replies to be analyzed, we extended the data analysis by seperating mentions from retweets as the nature of information they convey is different.  
# 
# 

# In[2]:


#Reads in the refined data to perform data analysis
pd.set_option('max_colwidth', 400)
df = pd.read_csv('./data/CleanedCometLanding.csv')


# In[3]:


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


# In[4]:


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
        


# In[5]:


''' This function returns the number of reply tweets '''
#Source:https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
def getNumberOfReplies(df):
     
    replies = df["in_reply_to_user_id_str"].notnull().sum()  
    
    return replies
    


# In[6]:


''' This function returns the number of general tweets'''
def getNumberOfGeneralTweets(df):
    mentions = getNumberOfMentionTweets(df)
    retweets = getNumberOfRetweets(df)
    replies = getNumberOfReplies(df)
    
    NumberOfGeneralTweets = len(df) - retweets - mentions - replies 
    return  NumberOfGeneralTweets


# In[7]:


''' This function returns total number of tweets'''
def getTotalNumberOfTweets(df):
    return len(df)


# In[8]:


''' This function returns the number of different users in the dataset'''
def getNumberOfDifferentUsers(df):
    differentUsers = df['from_user'].unique()
    return len(differentUsers)


# We decided to extend the calculate the average number of tweets, retweets and replies sent by a user requirement with calculating the average number of followers per user and calculating the average number of friends per user in order to gain a more representative idea about the population who interacted with this event. This gives an idea about whether people who interacted with this event was popular in twitter community.  

# In[9]:


''' This function prints data about the average user who interacted with this event''' 
def basicUserInteractionAnalysis(df):
    differentUsers = getNumberOfDifferentUsers(df)
    averageGeneralTweetsPerUser = getNumberOfGeneralTweets(df) / differentUsers
    averageMentionsPerUser = getNumberOfMentionTweets(df) / differentUsers
    averageRetweetsPerUser = getNumberOfRetweets(df) / differentUsers
    averageRepliesPerUser = getNumberOfReplies(df) / differentUsers
    averageFollowersPerUser = getTotalNumberOfUserFollowers(df) / differentUsers
    averageFriendsPerUser = getTotalNumberOfUserFollowers(df) / differentUsers
    
    print("The average number of general tweets per user is:", averageGeneralTweetsPerUser)
    print("The average number of mentions tweets per user is:", averageMentionsPerUser)
    print("The average number of retweets per user is:", averageRetweetsPerUser)
    print("The average number of replies per user is:", averageRepliesPerUser)
    print("The average number of followers per user is:", averageFollowersPerUser)
    print("The average number of friends per user is:", averageFriendsPerUser)
    


# In[10]:


''' This function prints the 5 most popular hashtags in the dataset''' 
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


# We believe it is important to have case insensitivity while analysing the hashtags because it will yield results where hashtags mean contextually different things and this can increase our undertstanding about the data

# In[11]:


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
            


# In[12]:


''' This function returns data about the popular times , days, and dates that the tweets were sent at'''
# Each time data is in user's local time, adjusting time data to be represented in one unit (such as GMT) is not
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
    


# In[13]:


'''This function returns the most popular user language'''
#While twitter supports 34 languages, we focused on the most commonly spoken languages for the scope of this practical
#elif structure assures no unnecessary checks were made
def getTweetDataAboutLanguage(df):
    languages = [] 
    languageColumn = df['user_lang']
    
    englishPattern = 'en'
    frenchPattern = 'fr'
    germanPattern = 'de'
    spanishPattern = 'es'
    chinesePattern = 'zh-cn'
    
    for (columnName, columnData) in languageColumn.iteritems():  
        matchList1 = re.search(englishPattern , str(columnData))
        matchList2 = re.search(frenchPattern , str(columnData))
        matchList3 = re.search(germanPattern , str(columnData))
        matchList4 = re.search(spanishPattern , str(columnData))
        matchList5 = re.search(chinesePattern , str(columnData))
        
        if matchList1 != None:
            languages.append('English')
        elif matchList2 != None:
            languages.append('French')
        elif matchList3 != None:
            languages.append('German')
        elif matchList4 != None:
            languages.append('Spanish')
        elif matchList5 != None:
            languages.append('Chinese')
        else:
            languages.append('Other')
        
        
    counterLanguages = collections.Counter(languages)
        
    newDataFrame = pd.DataFrame(counterLanguages.most_common(5))
    newDataFrame.to_csv('./data/Languages.csv',index = False, header=False)
        
    
        


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


def getTotalNumberOfUserFollowers(df):
    return (df['user_followers_count'].sum())


# In[17]:


def getTotalNumbersOfUserFriends(df):
    return (df['user_friends_count'].sum())


# In[18]:


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
    print('5 most popular apps to send tweets are', getMostPopularApplicationsUsed(df))
    getTweetDataAboutTime(df)
    getTweetDataAboutLanguage(df)


# In[19]:


performDataAnalysis(df)


# In[20]:


def main():

    pd.set_option('max_colwidth', 400)
    df = pd.read_csv('./data/CleanedCometLanding.csv')
    performDataAnalysis(df)

if __name__ == "__main__":
    main()

