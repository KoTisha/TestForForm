from django.db import models
from django.conf import settings

# Create your models here.

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=350, default="Not exist")
    message = models.TextField(max_length=10000, default="Not exist")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    isInWork = models.BooleanField(default=False)
    file = models.FileField(null=True, default=None)
    creationTime = models.DateTimeField(auto_now=False, auto_now_add=True)
