import tweepy
from tweepy import OAuthHandler
import re
import time
import sys

# Twitter key and token for OAuthen
consumer_key = '4DuxDJ4N2DwaUOvfzLPKYs6Dt'
consumer_secret = 'Ag43X1CBESRKzN4gIjmgl9Wy2rqQPAYhI8jcTNSBtD9RccbdPg'
access_token = '2368239648-0Qq4N5QvNnvmETRzXg8aDaCECTuvCLgC1UoL8dw'
access_secret = 'Sv3MjMaNz88UStJQourZymdpudIe6XJcea7ppYP2nQRdP'

# User authentication
# auth = OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_secret)

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# print api.rate_limit_status()['resources']['search']
# sys.exit(0)

# For index tweet
maxID = -1

# Get how many tweet
tweetsPerQry = 100
maxTweets = 10000
tweetCount = 0

trendList = []
while True:
    for trendLabel in api.trends_place(23424977)[0]['trends']:
        if trendLabel['name'] not in trendList:
            trendList.append(trendLabel['name'])
            keyword = re.sub('\W+','', trendLabel['name'])
            searchQuery = trendLabel['name']
            f = open(keyword+".csv", "w")

            tweetList = []
            maxAttempt = 10
            attempt = 0
            while tweetCount < maxTweets:
                try:
                    if maxID <= 0:
                        newTweets = api.search(q=searchQuery, rpp=tweetsPerQry, lang='en', tweet_mode='extended')
                    else:
                        newTweets = api.search(q=searchQuery, rpp=tweetsPerQry, max_id=maxID, lang='en', tweet_mode='extended')

                    if not newTweets:
                        print "No more tweets found"
                        break

                    else:
                        for tweet in newTweets:
                            # from pprint import pprint
                            # pprint(dir(tweet))
                            # sys.exit(0)
                            if not tweet.retweeted and "RT @" not in tweet.full_text:
                                cleanText = " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.full_text).split())
                                if len(cleanText.split()) > 0 and cleanText not in tweetList:
                                    tweetList.append(cleanText)
                                    tweetCount += 1
                                    print "{0:3}, {1:20}, {2}".format(tweet.retweet_count, tweet.user.id, cleanText)
                                    f.write("{0},{1},{2},{3}\n".format(searchQuery, tweet.retweet_count, tweet.user.id, cleanText))

                        print("Downloaded {0} tweets".format(tweetCount))
                        maxID = newTweets[-1].id - 1

                except tweepy.TweepError as e:
                    print("Error : " + str(e))
                    time.sleep(60)
            f.close()
    time.sleep(6000)

