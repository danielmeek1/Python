#!/usr/bin/env python3

import csv

filePath = "../data/CometLanding.csv"
outputfile = "../data/CometLandingCleaned.csv"

ids = set()

def cleanLine(line):
 
    valid = True

    id = line.split(",")[0]

    if id in ids or len(id) != 18 or  len(line.split(",")) < 17 :
        valid = False

    if(valid):
        ids.add(line.split(",")[0])
        with open(outputfile, 'a') as output:
            output.write(line)
            
def main():
    open(outputfile, 'w').close()

    landingData = open(filePath)
    lines = landingData.readlines()
    
    for line in lines:
        cleanLine(line)

if __name__ == "__main__":
    main()

