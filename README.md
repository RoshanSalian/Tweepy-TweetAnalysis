# Tweepy-TweetAnalysis
Script to extract tweets from Twitter API and analyse them into positive, negative and neutral

Requires package:
  - Tweepy 
  - TextBlob
  
Extracts most recent 3240 tweets having the user defined keyword from Twitter API and sends it to TextBlob for analysis. TextBlob categorizes tweets into positive, negative and neutral and saves this count in a text file inside a directoty named the keyword entered by the user. 
Requires user to get the access tocken and twitter key by registering on https://apps.twitter.com/
