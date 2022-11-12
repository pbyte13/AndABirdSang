from datetime import timedelta
from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
import requests
from requests import post, put, get

BASE_URL = "https://api.spotify.com/v1/"

def get_spotify_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]


def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_spotify_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])

    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token, refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()

def is_spotify_authenticated(session_id):
    tokens = get_spotify_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(tokens)
        return True
    return False


def refresh_spotify_token(session_id):
    refresh_token = get_spotify_user_tokens(session_id).refresh_token
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')

    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)

def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    tokens = get_spotify_user_tokens(session_id)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + tokens.access_token}

    if post_:
        post(BASE_URL + endpoint, headers=headers)
    if put_:
        put(BASE_URL + endpoint, headers=headers)

    response = get(BASE_URL + endpoint, {}, headers=headers)
    try:
        return response.json()
    except:
        return {'Error': 'Issue with request.'}

def get_spotify_user_id(session_id):
    '''We need ID to make a playlist.'''
    
    tokens = get_spotify_user_tokens(session_id)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + tokens.access_token}
    response = get("https://api.spotify.com/v1/me", headers=headers).json()

    try:
        return response.get('id')
    except:
        return {'Error': 'Issue with request.'}

def get_playlist_uris(session_id, playlist_id):
    '''Returns list of all tracks in a given playlist.'''

    #   HOUSEKEEPING

    tokens = get_spotify_user_tokens(session_id)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + tokens.access_token}

    #   GET PLAYLIST LENGTH (TO DEAL W/PAGINATION)

    playlist_info_endpoint = "https://api.spotify.com/v1/playlists/" + str(playlist_id)
    playlist_length = requests.get(playlist_info_endpoint, headers=headers).json().get('tracks').get('total')

    #   GET ALL TRACKS

    uris = []

    playlist_tracks_endpoint = "https://api.spotify.com/v1/playlists/" + str(playlist_id) + "/tracks"

    for i in range(int(playlist_length / 50) + 1):      #   EX. if there are 189 songs, you have to make 4 requests ...

        params = {'limit': 50, 'offset': i * 50}
        tracks = requests.get(playlist_tracks_endpoint, headers=headers, params=params).json().get('items')

        for track in tracks:
            uris.append(track.get('track').get('uri'))

    return uris



