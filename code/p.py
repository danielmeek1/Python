#!/usr/bin/env python3

import csv
import pandas as pd

filePath = "../data/CometLanding.csv"
outputfile = "../data/CometLandingCleaned.csv"

ids = set()

def cleanData(data):
 
    data.drop_duplicates(subset=['status_url'], keep='first')

    

            
def main():

    landingData = pd.read_csv( filePath, header=0)

    cleanData(landingData)

    landingData.to_csv(outputfile, index=False, encoding='utf-8')


if __name__ == "__main__":
    main()

