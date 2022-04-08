#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import math


# In[2]:


pd.set_option('max_colwidth', 400)


# In[3]:


df = pd.read_csv('./data/CometLanding.csv')


# # Data Refinement Justifications
# 
# In order to refine the data, we first had to know the structure of the data. Therefore, we did research on the Twitter API through resources Twitter provides for developers. After this research process, we have identified the dataset structure and we have defined functions that would check whether the data we were given is in the specified structure. 
# 
# It's our view that any tweet data that doesn't follow the tweet structure can not be viewed as a valid tweet and it can't be trusted. Therefore, to achieve correctness in data analysis we have removed the data that was inconsistent with the structure from our dataset. 
# 
# In this project, we focused on reproducibility so that our project would be able to analyze any tweet data no matter what the context is. Therefore, we completely avoided doing any kind of manual checking. All of the functions we have defined in data refinement work on tweet objects which are universal to any tweet data. 
# 
# Furthermore, it was also crucial for us to have a repetable code to make sure that we minimize unnecessary frictions and distractions during our development process to avoid having bugs in our code. Hence, we organized the functions according to what tweet object the function works on. 
# 
# Lastly, this structuring of our code alongside using very well known and robust frameworks such as pandas makes sure the code can be used in other settings with minimal change.
# 

# In[4]:


''' This function removes any duplicate data  '''
def basicDataCleaning(df):
    df = df.drop_duplicates(keep = 'first')
    df = df.drop_duplicates(subset=['id_str'], keep='first')
    return df


# In[5]:


''' This function asserts that the user name follows the specified data format in the Twitter API'''
''' Source:https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet'''
''' Usernames that are longer than 15 Characters are not valid '''
''' Usernames that contain non-alphanumeric characters are not valid with the exception of underscores '''
''' Usernames containing the words Twitter or Admin are not valid  '''

def validateUserName(df):
    
    df = df.drop(df[df['from_user'].str.len() > 15].index)  
    df = df.drop(df[df['from_user'].apply(lambda x: re.search(r'[a-zA-Z0-9_]', str(x)) == None)].index)
    df = df.drop(df[df['from_user'].apply(lambda x: re.search(r'Twitter', str(x), re.IGNORECASE) != None)].index)
    df = df.drop(df[df['from_user'].apply(lambda x: re.search(r'Admin', str(x), re.IGNORECASE) != None)].index)                 
    return df


# In[6]:


''' This function processes language data to achieve uniformity to ease data analysis'''
''' Turns data such as 'en-gb' to 'en' only to achieve consistency'''
''' Turns all data lower-case to achieve consistency'''

def refineLanguageData(df):
    df['user_lang'] = df['user_lang'].str.lower()
    df['user_lang'] = df["user_lang"].replace({'en-gb':'en'}, regex=True)
    return df


# In[7]:


'''This function asserts that the tweet length is within the parameters set in Twitter API'''
'''Although the maximum tweet length is 280 characters today
tweets could contain maximum 140 characters before November 8th 2017 (our data is from 2014)'''
'''Any tweet that is longer than 140 characters are removed'''
def validateTweetLength(df):
    
    df = df.drop(df[df['text'].str.len() > 140].index)
    return df


# In[8]:


'''This Function removes the data that do not follow twitter specifications for tweet replies'''
'''If a tweet is a reply, in_reply_to_user_id_str and in_reply_to_status_id_str must be not null'''
'''Source:https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet'''
#https://thispointer.com/pandas-4-ways-to-check-if-a-dataframe-is-empty-in-python/#:~:text=Check%20if%20dataframe%20is%20empty%20using%20Dataframe.&text=If%20our%20dataframe%20is%20empty,is%200%20in%20this%20tuple.

def validateReplyConsistency(df):
    
    for namedTuple in df.itertuples():
        in_reply_to_user_id_str = namedTuple[8]
        in_reply_to_status_id_str = namedTuple[11]

        if math.isnan(in_reply_to_user_id_str) == True and math.isnan(in_reply_to_status_id_str) == False:
            df = df.drop(namedTuple)    
        elif math.isnan(in_reply_to_user_id_str) == True and math.isnan(in_reply_to_status_id_str) == False:
            df = df.drop(namedTuple)
            
    return df


# In[9]:


''' This function creates new CSV file with the cleaned dataset to use in analysis ''' 
def createCleanedCSV(df):
    df.to_csv("./data/CleanedCometLanding.csv", index=False)


# In[10]:


''' This function calls all of the functions to refine the dataset and save refined data into a seperate csv file'''
def refineDataset(df):
    df1 = basicDataCleaning(df)
    df2 = validateUserName(df1)
    df3 = refineLanguageData(df2)
    df4 = validateTweetLength(df3)
    df5 = validateReplyConsistency(df4)
    df6 = validateReplyConsistency(df5)
    createCleanedCSV(df6)


# In[11]:


refineDataset(df)


# In[12]:


#def main():
    #77319 rows × 17 columns original data
    #df = pd.read_csv('CometLanding.csv')
    #refineDataset(df)
    

#if __name__ == "__main__":
    #main()

