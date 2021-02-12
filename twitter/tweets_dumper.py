import tweepy
import pandas as pd
from config import Config as cfg
import csv
from tqdm import tqdm

class TwitterClient(object):
    """
    Generic Twitter class for the app
    """

    def __init__(self, query):
        # twitter apps keys and tokens
        consumer_key = cfg['consumer_key']
        consumer_secret = cfg['consumer_secret']
        access_token = cfg['access_key']
        access_token_secret = cfg['access_secret']

        # Attempt authentication
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.query = query
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.tweet_count_max = 100  # To prevent Rate Limiting
        try:
            self.api.verify_credentials()
            print("Authentication successful!")
        except:
            print("Error: Authentication Failed")

    def get_home_timeline(self):
        timeline = self.api.home_timeline()
        for tweet in timeline:
            print(f"{tweet.user.name} said {tweet.text}")

    def get_user_details(self, user='yum_dude'):
        user = self.api.get_user(self.user)
        print("User details:")
        print(user.name)
        print(user.description)
        print(user.location)

    # def clean_tweet(self, tweet):
    #     return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweets(self):
        tweets = pd.DataFrame(columns=['user','tweet','created_at','favorite_count','geo',
            'id','is_quote_status','lang','retweet_count','source','url'])

        # insert column names as 1st row so as to have dataframe save line by line in append mode 
        tweets.loc[0, :] = 'user','tweet','created_at','favorite_count','geo','id','is_quote_status','lang','retweet_count','source','url'
        tweets.loc[[0]].to_csv('tweets_'+self.query.replace(' ','_')+'.csv', mode='a', index=False, header=False)

        try:
            recd_tweets = self.api.search(q=self.query, count=self.tweet_count_max)

            if not recd_tweets:
                pass
            for tweet in tqdm(recd_tweets):
                tweets.loc[tweet.id, 'user'] = tweet.user.screen_name
                tweets.loc[tweet.id, 'tweet'] = tweet.text
                tweets.loc[tweet.id, 'created_at'] = tweet.created_at
                tweets.loc[tweet.id, 'favorite_count'] = tweet.favorite_count
                tweets.loc[tweet.id, 'geo'] = tweet.geo
                tweets.loc[tweet.id, 'id'] = tweet.id
                tweets.loc[tweet.id, 'is_quote_status'] = tweet.is_quote_status
                tweets.loc[tweet.id, 'lang'] = tweet.lang
                tweets.loc[tweet.id, 'retweet_count'] = tweet.retweet_count
                tweets.loc[tweet.id, 'source'] = tweet.source_url
                tweets.loc[tweet.id, 'url'] = "https://twitter.com/twitter/statuses/" + tweet.id_str

                # save to csv
                tweets.loc[[tweet.id]].to_csv('tweets_'+self.query.replace(' ','_')+'.csv', mode='a', index=False, header=False)

            # save the id of the second-last tweet 
            oldest = recd_tweets[-1].id - 1

            # keep grabbing tweets until there are no more tweets left to grab
            while len(recd_tweets) > 0:
                print('getting tweets before %s' % (oldest))

                recd_tweets = self.api.search(q=self.query, count=self.tweet_count_max, max_id=oldest)

                for tweet in tqdm(recd_tweets):
                    tweets.loc[tweet.id, 'user'] = tweet.user.screen_name
                    tweets.loc[tweet.id, 'tweet'] = tweet.text
                    tweets.loc[tweet.id, 'created_at'] = tweet.created_at
                    tweets.loc[tweet.id, 'favorite_count'] = tweet.favorite_count
                    tweets.loc[tweet.id, 'geo'] = tweet.geo
                    tweets.loc[tweet.id, 'id'] = tweet.id
                    tweets.loc[tweet.id, 'is_quote_status'] = tweet.is_quote_status
                    tweets.loc[tweet.id, 'lang'] = tweet.lang
                    tweets.loc[tweet.id, 'retweet_count'] = tweet.retweet_count
                    tweets.loc[tweet.id, 'source'] = tweet.source_url
                    tweets.loc[tweet.id, 'url'] = "https://twitter.com/twitter/statuses/" + tweet.id_str

                    # save to csv
                    tweets.loc[[tweet.id]].to_csv('tweets_'+self.query.replace(' ','_')+'.csv', mode='a', index=False, header=False)

                # update the id of oldest with the second-last tweet's id 
                oldest = recd_tweets[-1].id - 1

                if len(recd_tweets) < 100:
                    break
            
            return 1

        except tweepy.TweepError as e:
            print("Error : " + str(e))


if __name__=="__main__":

    api = TwitterClient('yum_dude')
    tweets = api.get_tweets()
