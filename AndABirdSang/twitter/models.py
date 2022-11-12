from django.db import models

class TwitterToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    access_token = models.CharField(max_length=100)
    access_token_secret = models.CharField(max_length=100)

class TaskData(models.Model):
    task_id = models.CharField(max_length=1000)
    friend_count = models.IntegerField()
    progress_count = models.IntegerField()


