from django.shortcuts import redirect, render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from requests import post, Request, get
from .credentials import api_key, api_key_secret
from rest_framework import status
from .utils import update_or_create_user_tokens, get_twitter_user_tokens
from rest_framework.views import APIView
from .models import TaskData
import tweepy
import os 

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
oauth1_user_handler = tweepy.OAuth1UserHandler(api_key, api_key_secret, callback='http://127.0.0.1:8000/twitter/redirect')

class AuthURL(APIView):
    def get(self, request, format=None):
        #oauth1_user_handler = tweepy.OAuth1UserHandler(api_key, api_key_secret, callback='http://127.0.0.1:8000/twitter/redirect')
        url = oauth1_user_handler.get_authorization_url(signin_with_twitter=True)
        return redirect(url)

def twitter_callback(request):

    oauth_verifier = request.GET.get('oauth_verifier')
    oauth_token = request.GET.get('oauth_token')

    access_token, access_token_secret = oauth1_user_handler.get_access_token(oauth_verifier)

    #   DID NOT VERIFY USER TOKENS ...

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(
        request.session.session_key,
        access_token=access_token,
        access_token_secret=access_token_secret)

    return redirect('/create')


class GetProgress(APIView):
    '''Returns value MUI can use to configure progress bar.'''

    def get(self, request, **kwargs):

        task_id = self.kwargs['taskID']
        task = TaskData.objects.get(task_id=task_id)
        progress_count = task.progress_count
        friend_count = task.friend_count

        progress = (progress_count / friend_count) * 100

        return Response({'progress': progress}, status=status.HTTP_200_OK)

