import tweepy

# crawling from twitter


# authorization level
API_KEY = 'NjHC0Y2Iql94ivUB78lC60Bpm'
API_SECRET = 'mR4R132jKjuUga5GN0RyVngVk80I23daJhR21n1RstQDQvZNG6'
ACCESS_KEY = '794856483007533057-n4iG19CHb8KNvxIkmSp1ahg7mPhe0Bq'
ACCESS_SECRET = '2Pp0aZBou8DQ2h6y0ptim6Zo1F3HlLmOAxhG5sVuN2EY2'

oAuth = tweepy.OAuthHandler(API_KEY, API_SECRET)
oAuth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth_handler=oAuth, api_root='/1.1')

# search timeline through ID keyword
userID = "sehee0517"
user = api.get_user(userID)
print user.id

l = user.followers()

for i in l:
    print i.id