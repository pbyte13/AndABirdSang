
from .models import TwitterToken
from .credentials import api_key, api_key_secret, access_token, access_token_secret, bearer_token
import tweepy
import twint

def get_twitter_user_tokens(session_id):
    user_tokens = TwitterToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]

def update_or_create_user_tokens(session_id, access_token, access_token_secret):
    tokens = get_twitter_user_tokens(session_id)

    if tokens:
        tokens.access_token = access_token
        tokens.access_token_secret = access_token_secret
        tokens.save(update_fields=['access_token', 'access_token_secret'])

    else:
        tokens = TwitterToken(user=session_id, access_token=access_token, access_token_secret=access_token_secret)
        tokens.save()

def get_friends(session_id):
    '''Get the friends of the authenticated user.'''

    tokens = get_twitter_user_tokens(session_id)
    user_access_token = tokens.access_token
    user_access_token_secret = tokens.access_token_secret
    auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, user_access_token, user_access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    screen_name = api.verify_credentials().screen_name
    #user_id = api.get_user(screen_name)
    friends = api.get_friend_ids(screen_name=screen_name)

    return friends

def get_protected_users(session_id, friends):
    '''Returns a list of friends (ids) that have protected tweets.'''
    
    tokens = get_twitter_user_tokens(session_id)
    user_access_token = tokens.access_token
    user_access_token_secret = tokens.access_token_secret
    auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, user_access_token, user_access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    protected_users = []

    for friend in friends:
        try:
            if api.get_user(user_id=friend)._json['protected'] == True:
                protected_users.append(friend)
        except:
            continue
    
    return protected_users

def get_user_songs_api(session_id, user_id):
    '''Get Spotify URIs from any given user.'''
    
    tokens = get_twitter_user_tokens(session_id)
    user_access_token = tokens.access_token
    user_access_token_secret = tokens.access_token_secret
    auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, user_access_token, user_access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    screen_name = api.verify_credentials().screen_name

    client = tweepy.Client(
        bearer_token=bearer_token, 
        consumer_key=api_key, 
        consumer_secret=api_key_secret, 
        access_token=access_token, 
        access_token_secret=access_token_secret)

    start_time = "2022-09-11T00:00:00Z"
    
    json_objects = [api.get_status(tweet.id)._json for tweet in tweepy.Paginator(client.get_users_tweets, user_id, start_time=start_time, exclude=['replies','retweets']).flatten(limit=30)]
    
    expanded_urls = [json_object['entities']['urls'][0]['expanded_url'] for json_object in json_objects if json_object['entities']['urls']]
    spotify_urls = [expanded_url for expanded_url in expanded_urls if 'spotify.com/track' in expanded_url]
    spotify_uris = ["spotify:track:" + spotify_url[spotify_url.find("track/") + 6: spotify_url.find("?")] for spotify_url in spotify_urls] 
    
    return spotify_uris


def get_user_songs_twint(user_id):

    config = twint.Config()
    config.User_id = str(user_id)
    config.Since = "2022-10-01"
    config.Store_object = True
    config.Search = 'url:open.spotify.com/track'

    twint.run.Search(config)
    tweets = twint.output.tweets_list

    spotify_urls = [tweet.urls[0] for tweet in tweets]
    spotify_uris = ["spotify:track:" + spotify_url[spotify_url.find("track/") + 6: spotify_url.find("?")] for spotify_url in spotify_urls] 
    
    return spotify_uris

def get_all_songs(session_id):

    tokens = get_twitter_user_tokens(session_id)
    user_access_token = tokens.access_token
    user_access_token_secret = tokens.access_token_secret
    auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, user_access_token, user_access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    screen_name = api.verify_credentials().screen_name

    client = tweepy.Client(
        bearer_token=bearer_token, 
        consumer_key=api_key, 
        consumer_secret=api_key_secret, 
        access_token=access_token, 
        access_token_secret=access_token_secret)

    songs = [[]]  #   changed this from []

    ###     GET SONGS FROM PROTECTED FRIENDS     ###

    friends = get_friends(session_id)
    protected_friends = get_protected_users(session_id, friends)

    counter = 0

    for friend in protected_friends:
        print("protected" + str(counter))
        counter += 1
        uris = get_user_songs_api(session_id, friend)
        if len(uris) + len(songs[-1]) > 100:            #   "A maximum of 100 items can be added in one request."
            songs.append(uris)
        else:
            for uri in uris:
                songs[-1].append(uri)

    ###     GET SONGS FROM ALL OTHER FRIENDS     ###
    count = 0

    other_friends_songs = []

    for friend in friends:
        count += 1
        print(count)
        try:
            uris = get_user_songs_twint(friend)
            for uri in uris:
                other_friends_songs.append(uri)
        except:
            continue
        
    unique = set(other_friends_songs)

    for song in unique:
        if len(songs[-1]) == 100:            #   "A maximum of 100 items can be added in one request."
            songs.append([song])
        else:
            songs[-1].append(song)

    return songs






