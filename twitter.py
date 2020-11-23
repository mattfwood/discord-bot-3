import tweepy
import os
import pprint

from random import choice
from dotenv import load_dotenv

load_dotenv()

pp = pprint.PrettyPrinter(indent=2)


def get_key(name):
    return os.environ.get(name)


auth = tweepy.OAuthHandler(
    get_key('TWITTER_CONSUMER_KEY'), get_key('TWITTER_CONSUMER_TOKEN')
)
auth.set_access_token(
    get_key('TWITTER_ACCESS_TOKEN'), get_key('TWITTER_ACCESS_TOKEN_SECRET')
)

twitter = tweepy.API(auth)


def get_random_tweet(username):
    tweets = twitter.user_timeline(username)
    originals = []

    # pp.pprint(tweets[13]._json)

    for tweet in tweets:
        # remove tweet replies and responses
        if tweet.text[0] != '@' and tweet._json['in_reply_to_screen_name'] == None:
            originals.append(tweet)

    result = choice(originals)

    return f"https://twitter.com/{username}/status/{result._json['id']}"


# print(get_random_tweet('dril'))