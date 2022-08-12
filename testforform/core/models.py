from asyncio.windows_events import NULL
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Person(User):

    class Meta():
        proxy = True
        permissions = [
            ("can_create_feedback", "Can create feedback messenges"),
        ]

class Manager(User):
    class Meta():
        proxy = True
        permissions = [
            ("can_check_feedback", "Can checking feedback from Users"),
            ("can_work_with_feedback", "Can edit feedback"),
        ]

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=350, default="Not exist")
    message = models.TextField(max_length=10000, default="Not exist")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    isInWork = models.BooleanField(default=False)
    file = models.FileField(null=True, default=NULL)
    creationTime = models.DateTimeField(auto_now=False, auto_now_add=True)
