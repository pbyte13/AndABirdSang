import requests, json
from audioop import add
from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_ID, CLIENT_SECRET
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import *
from twitter.tasks import create_playlist_task
from twitter.models import TaskData

BASE_URL = "https://api.spotify.com/v1/"

class AuthURL(APIView):
    def get(self, request, format=None):

        request.session.flush()

        scopes = "playlist-modify-private playlist-modify-public user-read-private"
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)

def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()


    update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)
    
    return redirect('/twitter/get-auth-url')

class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)

class CreatePlaylist(APIView):
    def get(self, request, format=None):

        playlist = create_playlist_task.delay(self.request.session.session_key)  #   CELERY
        task_id = playlist.task_id

        t = TaskData(task_id=task_id, friend_count=1000, progress_count=0)
        t.save()

        url = '/progress/' + str(task_id)

        return Response({'url': url}, status=status.HTTP_200_OK)


        

