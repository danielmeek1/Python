import DataRefinement as refine
import DataAnalysis as analysis
import pandas as pd
import unittest

class TestDataRefinement(unittest.TestCase):


    def test_BasicDataCleaning(self):
        pd.set_option('max_colwidth', 400)
        df = pd.read_csv('./data/CometLanding.csv')
        df = df.head(10)
        df = refine.basicDataCleaning(df)
        self.assertEqual(len(df), 9)

    def test_validateuserName(self):
        pd.set_option('max_colwidth', 400)
        df = pd.read_csv('./data/CometLanding.csv')
        df = df.head(10)
        df = refine.validateUserName(df)
        self.assertEqual(len(df), 8)

    def test_refineLanguageData(self):
        pd.set_option('max_colwidth', 400)
        df = pd.read_csv('./data/CometLanding.csv')
        df = df.head(10)
        df = refine.refineLanguageData(df)    
        for row in df.iterrows():
            self.assertTrue(row[1]['user_lang']== 'en' or row[1]['user_lang']== 'fr')
    
    def test_getNumberOfMentionTweets(self):
        pd.set_option('max_colwidth', 400)
        df = pd.read_csv('./data/CometLanding.csv')
        df = df.head(10)
        df = analysis.getNumberOfMentionTweets(df)
        self.assertEqual(df, 1)
    
    def test_getNumberOfRetweets(self):
        pd.set_option('max_colwidth', 400)
        df = pd.read_csv('./data/CometLanding.csv')
        df = df.head(10)
        df = analysis.getNumberOfRetweets(df)
        self.assertEqual(df, 7)
    
    def test_getNumberOfReplies(self):
        pd.set_option('max_colwidth', 400)
        df = pd.read_csv('./data/CometLanding.csv')
        df = df.head(10)
        df = analysis.getNumberOfReplies(df)
        self.assertEqual(df,0)
    


if __name__ == '__main__':
    unittest.main()