try:
    import json
except ImportError:
    import simplejson as json
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import twitter

def main():
    ACCESS_TOKEN = '929922426615615488-LEnsfpKHxyUFP4I2mfMKJXzwvigEGqW'
    ACCESS_SECRET = 'eYYHhi2ECZxQtBkXjsWARpSjXYBa1Yjca3onwObVFS0he'
    CONSUMER_KEY = 'LpXysFFUZ24YOBGYlc269Gcp7'
    CONSUMER_SECRET = 'LdI6m8O93vwWRJZarNMOB6KJ9pycbXMrkEa9DqfIwKSTNjbsN7'
    oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
    api=Twitter(auth=oauth)
    twitter_stream = TwitterStream(auth=oauth)
    iterator = twitter_stream.statuses.filter(track="I'm sorry", language="en")
    bigToSmall=0
    smallToBig=0
    same=0
    avgUser=0
    avgOther=0
    numTweets=0
    for tweet in iterator:
        try:
            j=json.dumps(tweet)
            tweet = json.loads(j.strip())
            if 'text' in tweet: # only messages contains 'text' field is a tweet
                if tweet['text'].find("@") !=-1:
                    print tweet['user']['screen_name']
                    print tweet['text'] # content of the tweet
                    print "Number of followers of user: ", tweet['user']['followers_count']
                    text=tweet['text']
                    text=text[text.find("@"):]
                    userName=text[1:text.find(" ")]
                    numTweets+=1
                    try:
                        user= api.users.lookup(screen_name=userName)
                        j=json.dumps(user)
                        userProf = json.loads(j.strip())
                        print "Number of followers of ", userName, ": ", userProf[0]['followers_count']
                        typeOF=findTypeOfInter(tweet['user']['followers_count'],  userProf[0]['followers_count'])
                        avgUser+=int(tweet['user']['followers_count'])
                        avgOther+=int(userProf[0]['followers_count'])
                        print "Average of people reconciling: ", avgUser/numTweets
                        print "Average of other person: ", avgOther/numTweets
                        if(typeOF==0):
                            smallToBig+=1
                        elif(typeOF==1):
                            same+=1
                        else:
                            bigToSmall+=1
                        print "Left :", smallToBig, "Middle: ", same, "Right: ", bigToSmall
                        #print api.show_friendship(userName,tweet['user']['screen_name'])
                    except:
                        userName=text[1:text.find(" ")-1]
                        user= api.users.lookup(screen_name=userName)
                        j=json.dumps(user)
                        userProf = json.loads(j.strip())
                        print "Number of followers of ", userName, ": ", userProf[0]['followers_count']
                        typeOF= findTypeOfInter(tweet['user']['followers_count'],  userProf[0]['followers_count'])
                        avgUser+=int(tweet['user']['followers_count'])
                        avgOther+=int(userProf[0]['followers_count'])
                        print "Average of people reconciling: ", avgUser/numTweets
                        print "Average of other person: ", avgOther/numTweets
                        if(typeOF==0):
                            smallToBig+=1
                        elif(typeOF==1):
                            same+=1
                        else:
                            bigToSmall+=1
                        print "Left :", smallToBig, "Middle: ", same, "Right: ", bigToSmall
                        #print api.show_friendship(userName,tweet['user']['screen_name'])
        except:
            continue
def findTypeOfInter(userCount, otherCount):
    typeUser=int(userCount)
    if(typeUser>=8000):
        typeUser=2
    elif(typeUser>=3000):
        typeUser=1
    else:
        typeUser=0
    typeOther=int(otherCount)

    if(typeOther>=8000):
        typeOther=2
    elif(typeOther>=3000):
        typeOther=1
    else:
        typeOther=0
    typeOfInter=0
    if(abs(int(userCount)-int(otherCount))<100):
        typeOfInter=1
    elif(typeOther>typeUser):
        typeOfInter=0
    elif(typeOther<typeUser):
        typeOfInter=2
    elif(typeOther==typeUser):
        typeOfInter=1
    return typeOfInter

if __name__ == "__main__":
    main()