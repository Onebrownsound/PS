import tweepy
import time
import re

CONSUMER_KEY = 'f1vJ5dpjmFKnlCFonzX1gW7Ld'
CONSUMER_SECRET = 'QtPUNrkahIzd09U09ofir6q2WhuMuGaeuHG5TZLimDWpQLqdUS'
ACCESS_TOKEN = '712093272785735680-faAaPFyZDHw1yZwJ1lVbZ6oxK6D30JA'
ACCESS_SECRET = 'ty1rGzL3CtWmxbXmMWJbMkefugkfnnMFhES7y2QHqj0qu'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)
        with open('garbage_tweets.txt', 'ab') as f:
            tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ",
                                    status.text).split())  # cleanup tweets
            tweet += '\n'
            f.write(tweet.encode("UTF-8"))


def search_Twitter(query):
    result = [tweet.text for tweet in (tweepy.Cursor(api.search, q=query, lang='en', count=100).items())]
    return result


def collectTweets(tweet_file_name, query_string):
    while (True):
        print('Scraping more data...')
        try:
            tweets = search_Twitter(query_string)
            with open(tweet_file_name + '.txt', 'ab') as f:
                for tweet in tweets:
                    tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ",
                                            tweet).split())  # cleanup tweets
                    tweet += '\n'
                    f.write(tweet.encode("UTF-8"))

            print('Wrote to file..sleeping for 15 minutes')
            time.sleep(60 * 1)
        except tweepy.TweepError as e:

            print('Error {0} {1}'.format(e.reason, e.response))
            time.sleep(60 * 1)


collectTweets('death_tweets', "condolences sorry for your loss")




# myStreamListener = MyStreamListener()
# myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
# myStream.filter(track=['twitter', 'RT'], async=True, languages=['en'])
