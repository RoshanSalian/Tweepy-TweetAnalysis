import re
import os
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    def __init__(self):
        # Twitter Key
        consumer_key =
        consumer_secret =

        # Twitter Access Token
        access_token =
        access_token_secret = 

        try:
            # Twitter Authentication
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)

            # Twitter Api Connection
            self.api = tweepy.API(self.auth)

        except:
            print("Authentication Failed")

    def clean_tweet(self, tweet):
        # Remove extra character
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        # Analysis of tweet by making a call to TextBlob API
        analysis = TextBlob(self.clean_tweet(tweet))

        # Categorize text into positive, negative, neutral
        if analysis.sentiment.polarity > 0:
            return 'positive';
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    # Fetching of tweets
    # Twitter only allows access to a user most recent 3240 tweets
    def get_tweets(self, query, count=10):
        # List to hold all tweepy tweets
        tweets = []
        try:
            fetched_tweet = self.api.search(q=query, count=count)

            for tweet in fetched_tweet:
                parsed_tweet = {}

                parsed_tweet['text']=tweet.text

                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # To remove redundancy
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets
        except tweepy.TweepError as e:
            print('Error' + str(e))


def main():
    # Call to twitter API
    api = TwitterClient()

    # Take keyword as input
    name = input('Enter Query: ')

    # Call to fetch tweets
    tweets = api.get_tweets(query=name, count=200)

    # Create directory in same folder
    if not os.path.exists(name):
        print('Creating Project: ' + name)
        os.makedirs(name)

    # Create text file inside the directory for storing results
    comment = os.path.join(name, 'comment.txt')

    ptweets = [tweet for tweet in tweets if tweet['sentiment']=='positive']
    print("Positive tweets percentage: {0:.2f} %".format(100 * len(ptweets) / len(tweets)))
    with open(comment, 'w') as f:
        f.write('Positive = ' + str(100 * len(ptweets) / len(tweets)) + '\n')

    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {0:.2f} %".format(100 * len(ntweets) / len(tweets)))
    with open(comment, 'a') as f:
        f.write('Negative = ' + str(100 * len(ntweets) / len(tweets)) + '\n')

    print("Neutral tweets percentage: {0:.2f} %".format(100 * (len(tweets)-len(ntweets)-len(ptweets)) / len(tweets)))
    with open(comment, 'a') as f:
        f.write('Neutral = ' + str(100 * (len(tweets)-len(ntweets)-len(ptweets)) / len(tweets)) + '\n')

    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
        # with open(comment, 'a') as f:
        #     f.write('Positive tweets: \n' + tweet['text'] + '\n')

    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])
        # with open(comment, 'a') as f:
        #     f.write('Negative tweets: \n' + tweet['text'] + '\n')


if __name__ == "__main__":
        main()



