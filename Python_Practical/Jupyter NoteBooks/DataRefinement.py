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


# In[4]:


df['in_reply_to_user_id_str'].empty


# In[5]:


''' Removes duplicates along with other basic data cleaning '''
def basicDataCleaning(df):
    df = df.drop_duplicates(subset=['status_url'], keep='first')
    df = df.replace({r'[^\x00-\x7F]+':''}, regex=True)
    #df = df.dropna()
    return df


# In[6]:


df = basicDataCleaning(df)


# In[7]:


''' Removes usernames that are not valid from the data set (according to Twitter specifications) '''
''' Usernames that are longer than 15 Characters are not valid '''
''' Usernames that are not alphanumeric are not valid with the exception of underscores '''
''' Usernames containing the words Twitter or Admin cannot be claimed. '''

def validateUserName(df):
    
    df = df.drop(df[df['from_user'].str.len() > 15].index)  
    df = df.drop(df[df['from_user'].apply(lambda x: re.search(r'[a-zA-Z0-9_]', x)) == None].index)
    df = df.drop(df[df['from_user'].apply(lambda x: re.search('Twitter', x, re.IGNORECASE) != None)].index)
    df = df.drop(df[df['from_user'].apply(lambda x: re.search('Admin', x, re.IGNORECASE) != None)].index)                 
    return df


# In[8]:


df = validateUserName(df)


# In[9]:


''' Refines language data '''
''' Turns data such as en-gb to en only to achieve consistency'''
''' Turns all data lower-case to achieve consistency'''

def refineLanguageData(df):
    df['user_lang'] = df['user_lang'].str.lower()
    df['user_lang'] = df["user_lang"].replace({'en-gb':'en'}, regex=True)
    return df


# In[10]:


df = refineLanguageData(df)


# In[11]:


'''Removes the data that do not follow twitter specifications for tweet length'''
'''A tweet could contain maximum 140 characters before November 8th 2017'''
'''Any data that do not match this specification is questionable'''
def validateTweetLength(df):
    
    df = df.drop(df[df['text'].str.len() > 140].index)
    return df


# In[12]:


df = validateTweetLength(df)


# In[13]:


'''Removes the data that do not follow twitter specifications for tweet reply'''
'''If a tweet is a reply, in_reply_to_user_id_str and in_reply_to_status_id_str must be not null'''
#Source:https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
#https://thispointer.com/pandas-4-ways-to-check-if-a-dataframe-is-empty-in-python/#:~:text=Check%20if%20dataframe%20is%20empty%20using%20Dataframe.&text=If%20our%20dataframe%20is%20empty,is%200%20in%20this%20tuple.
#not a number
#math.isnan()
def validateReplyConsistency(df):
    
    for namedTuple in df.itertuples():
        in_reply_to_user_id_str = namedTuple[8]
        in_reply_to_status_id_str = namedTuple[11]

        if math.isnan(in_reply_to_user_id_str) == True and math.isnan(in_reply_to_status_id_str) == False:
            df = df.drop(namedTuple)    
        elif math.isnan(in_reply_to_user_id_str) == True and math.isnan(in_reply_to_status_id_str) == False:
            df = df.drop(namedTuple)

    
    return df


# In[14]:


df = validateReplyConsistency(df)
#df1 = df.dropna(subset=cols


# In[15]:


''' Creates new CSV file with the cleaned dataset to use in analysis ''' 
def createCleanedCSV(df):
    df.to_csv("./data/CleanedCometLanding.csv", index=False)


# In[16]:


createCleanedCSV(df)


# In[ ]:


def main():
    #77319 rows × 17 columns original data
    df = pd.read_csv('CometLanding.csv')
    df = basicDataCleaning(df)
    

if __name__ == "__main__":
    main()

