import tweepy
from bluebird import BlueBird
import twint
consumer_key = ''
consumer_secret=''
access_token=''
access_token_secret=''
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit_notify=True,wait_on_rate_limit=True)

def ranking_algorithm(user):
#-----------------------------------------------------------------------
# Using the Twint module to fetch all the tweets by the influencer and store it in a list
#-----------------------------------------------------------------------
    c = twint.Config()
    c.Username = user
    #c.Limit = 5  #you can limit the number of responses, it gets all the responses by default
    c.Store_object = True
    c.Hide_output = True
    twint.run.Search(c) 
    tweets = twint.output.tweets_list 
    tweetid=[]
    dict= {}
#-----------------------------------------------------------------------
# Going through the tweet list, to get the influencer has mentioned, 
# adding in a dictionary and increasing score by 1
#-----------------------------------------------------------------------
    for tweet in tweets:  
        tweetid.append(tweet.id)  
        if tweet.mentions :
            for follower in tweet.mentions:   
                if follower in dict.keys():
                    dict[follower]+=1 
                else:
                    dict[follower]=1

#-----------------------------------------------------------------------
# #parsing all the tweets made by the influencer get followers who 
# retweeted and increasing their score by 1 in the dictionary
#-----------------------------------------------------------------------
    for id in tweetid:  
        retweets = api.retweets(id)
        for retweet in retweets:
            follower = retweet.user.screen_name
            if follower in dict.keys():
                dict[follower]+=1 
            else:
                dict[follower]=1

#-----------------------------------------------------------------------
# Getting all the followers who have replied to the influencer and 
# increasing their score by 1
#-----------------------------------------------------------------------
    
    replies = api.mentions_timeline()  # this API only runs for the authenticating user, in this case the influencer 
    for reply in replies:
        follower = reply.user.screen_name
        if follower in dict.keys():
            dict[follower]+=1 
        else:
            dict[follower]=1

#-----------------------------------------------------------------------
# sorting the dictionary in descending order by score
#-----------------------------------------------------------------------
    sort_dict = sorted(dict.items(), key=lambda x: x[1], reverse=True)

    return sort_dict


result = ranking_algorithm('balajis')
print(result)


def send_message(id, message):  
    api.send_direct_message(id, message)

def send_tweets(message, api):
    api.update_status(message)