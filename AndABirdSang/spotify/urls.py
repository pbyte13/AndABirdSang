from django.urls import path
from .views import AuthURL, spotify_callback, IsAuthenticated, CreatePlaylist

app_name = "spotify"

urlpatterns = [
    path('get-auth-url', AuthURL.as_view()),
    path('redirect', spotify_callback),
    path('is-authenticated', IsAuthenticated.as_view()),
    path('create-playlist', CreatePlaylist.as_view()),
    
]