import tweepy
import json
import requests

from .credentials import *
from celery import shared_task
from .models import TaskData
from django.shortcuts import redirect
from spotify.util import get_spotify_user_tokens, get_spotify_user_id, get_playlist_uris
from .utils import get_twitter_user_tokens, get_friends, get_protected_users, get_user_songs_api, get_user_songs_twint

BASE_URL = "https://api.spotify.com/v1/"

@shared_task(bind=True)
def create_playlist_task(self, session_id):
    
    tokens = get_spotify_user_tokens(session_id)
    user_id = get_spotify_user_id(session_id)
        
    #   HOUSEKEEPING:      Make requests to Spotify API

    playlists_endpoint = "users/" + user_id + "/playlists"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + tokens.access_token}
    create_body = json.dumps({'name': "AndABirdSang", 'description': "Music shared by those you follow on Twitter."})

    #   CHECK IF USER ALREADY HAS AN AndABirdSang PLAYLIST; IF NOT, CREATE NEW

    playlists = requests.get(BASE_URL + playlists_endpoint, headers=headers).json()

    playlist_id = None

    for item in playlists['items']:
        if item.get('name') == 'AndABirdSang':
            playlist_id = item.get('id') #  NEED TO CHANGE THIS LINE ....
            break

    if playlist_id == None:
        '''If none of the user's playlists were named AndABirdSang, create new playlist.'''
        response = requests.post(BASE_URL + playlists_endpoint, headers=headers, data=create_body).json()
        playlist_id = response.get('id')


    tokens = get_twitter_user_tokens(session_id)
    user_access_token = tokens.access_token
    user_access_token_secret = tokens.access_token_secret
    auth = tweepy.OAuth1UserHandler(api_key, api_key_secret, user_access_token, user_access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

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
    
    other_friends_songs = []

    #   create database entry to keep track of count

    task_id = create_playlist_task.request.id
    t = TaskData.objects.get(task_id=task_id)
    t.friend_count = len(friends)
    t.save()

    for friend in friends:

        task = TaskData.objects.get(task_id=task_id)
        progress_count = task.progress_count
        task.progress_count = progress_count + 1
        task.save()

        print(progress_count)

        try:
            uris = get_user_songs_twint(friend)
            for uri in uris:
                other_friends_songs.append(uri)
        except:
            continue
        
    unique = set(other_friends_songs)        #   for some reason we were getting duplicates of songs in prior twint tests

    for song in unique:
        if len(songs[-1]) == 100:            #   "A maximum of 100 items can be added in one request."
            songs.append([song])
        else:
            songs[-1].append(song)

    tokens = get_spotify_user_tokens(session_id)

    add_to_playlist_endpoint = "playlists/" + playlist_id + "/tracks"

    add_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + tokens.access_token}

    #   exclude songs already in user's playlist

    existing_songs = get_playlist_uris(session_id, playlist_id)

    new_songs = [[]]

    for l in songs:
        for song in l:
            if song not in existing_songs:
                if len(new_songs[-1]) == 100:
                    new_songs.append([song])
                else:
                    new_songs[-1].append(song)

    #   add songs to playlist
        
    for list in new_songs:
        add_body = json.dumps({'uris': list})
        r = requests.post(BASE_URL + add_to_playlist_endpoint, headers=add_headers, data=add_body).json()
        print(r)

    return redirect('/')