#!/usr/bin/env python
# coding: utf-8

# In[1]:


import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import re
import DataAnalysis as da


# In[2]:


pd.set_option('max_colwidth', 400)
df = pd.read_csv('./data/CleanedCometLanding.csv')


# In[3]:


''' This function returns the number of different users in the dataset'''
def getDifferentUsers(df):
    differentUsers = df['from_user'].unique()
    return (list(differentUsers))


# In[7]:


''' This function returns the lists for the edges in the network '''
'''  This function iterates the dataset and adds connections to the correct list'''
def getEdgesOfRetweets(df):

    userNameColumn = df['from_user']
    retweetEdges = []
    mentionsEdges = []
    repliesEdges = []
    
    #Itertuples has better execution performance than items() and iterrows()
    for namedTuple in df.itertuples():
        
        
        userName = namedTuple[2] #This is the username of the person sending the tweet
        tweet = namedTuple[3] #This is the tweet itself sent by the username above
        userBeingReplied = namedTuple[9] #This is given by the dataset if the tweet is a reply
        
        #If the tweet is a reply, in_reply_to_screen_name object will not be null
        if pd.isnull(namedTuple[9]) == False:
            repliesEdges.append((userName, userBeingReplied))
            
        #If the tweet is a retweet
        if re.search('RT @' , str(tweet))!= None:
            
            for word in tweet.split():
                extractionPattern = '(?<=@).*(?=:)'
                retweet = re.search(extractionPattern,word)
                if retweet != None:
                    retweetEdges.append((userName,retweet.group(0)))
            
        #If the tweet is a mention
        elif re.search ('@' , str(tweet))!= None:
    
            for word in tweet.split():
                extractionPattern = r'(?<=@).*(?=\b)'
                mention = re.search(extractionPattern,word)
                if mention != None:
                    mentionsEdges.append((userName,mention.group(0)))     
        
    return retweetEdges, mentionsEdges, repliesEdges


# In[8]:


''' This function returns the graph built from the nodes and edges returned from the functions above. '''
def drawNetwork(df):
    nodes = []
    nodes = da.getNumberOfDifferentUsers(df)
    
    retweetEdges, mentionsEdges, repliesEdges = getEdgesOfRetweets(df)
    
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(retweetEdges)
    G.add_edges_from(mentionsEdges)
    G.add_edges_from(repliesEdges)

    nx.draw_networkx(G)
    plt.show() 


# In[9]:


drawNetwork(df)


# In[ ]:




