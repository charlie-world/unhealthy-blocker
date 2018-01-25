import tweepy
from func_lib import *
from konlpy.tag import Twitter; t = Twitter()
from function import *
import time

# crawling from twitter

def twitterC(ID,flist,site_type):


    # authorization level
    API_KEY = 'NjHC0Y2Iql94ivUB78lC60Bpm'
    API_SECRET = 'mR4R132jKjuUga5GN0RyVngVk80I23daJhR21n1RstQDQvZNG6'
    ACCESS_KEY = '794856483007533057-n4iG19CHb8KNvxIkmSp1ahg7mPhe0Bq'
    ACCESS_SECRET = '2Pp0aZBou8DQ2h6y0ptim6Zo1F3HlLmOAxhG5sVuN2EY2'

    oAuth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    oAuth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth_handler=oAuth, api_root='/1.1')

    # search timeline through ID keyword
    userID = ID
    user = api.get_user(userID)
    timeline = api.user_timeline(userID)

    total_update(site_type)

    # GET USER'S TIMELINE TWEETS
    for tweet in timeline:
        try:
            texts = tweet.text
            texts = clean_text(texts)
            kkma = Twitter()
            t1 = kkma.nouns(texts)
            # GET the word by kkma

            # probability update
            for i in t1:
                print i

                # total update
                word_update(i, 1, site_type)

        except AttributeError as e:
            print(e)


    if site_type == 0:
        # SAVE USER'S FRIENDS IDs
        for friend in user.friends(count=200):
            flist.append(friend.id)
    else:
        for follower in user.followers():
            flist.append(follower.id)



