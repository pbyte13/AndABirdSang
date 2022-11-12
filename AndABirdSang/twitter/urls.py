from webbrowser import get
from django.urls import path
from frontend.views import index
from .views import AuthURL, twitter_callback, GetProgress

app_name = "twitter"

urlpatterns = [
    path('', index, name=''),
    path('get-auth-url', AuthURL.as_view()),
    path('redirect', twitter_callback),
    path('get-progress/<str:taskID>', GetProgress.as_view())
]