from django.urls import path
from .views import index

app_name = 'frontend'

urlpatterns = [
    path('', index, name=''),
    path('abird', index, name='abird'),
    path('how-it-works', index),
    path('link', index),
    path('create', index),
    path('progress/<str:taskID>', index)
]