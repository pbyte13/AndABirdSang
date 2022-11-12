import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AndABirdSang.settings")
app = Celery("AndABirdSang")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

