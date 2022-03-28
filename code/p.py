#!/usr/bin/env python3

import csv
import pandas as pd

filePath = "../data/CometLanding.csv"
outputfile = "../data/CometLandingCleaned.csv"

ids = set()

def cleanData(data):
 
    data = data.drop_duplicates(subset=['status_url'], keep='first')
    data = data.user_friends_count.notnull()
    data = data.text.replace({r'[^\x00-\x7F]+':''}, regex=True, inplace=True)
    
    data.to_csv(outputfile, index=False, encoding='utf-8')





    

            
def main():

    landingData = pd.read_csv( filePath, header=0)

    cleanData(landingData)

    


if __name__ == "__main__":
    main()

