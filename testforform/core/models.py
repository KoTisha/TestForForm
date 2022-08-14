from importlib.metadata import requires
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=350, default="Not exist")
    message = models.TextField(max_length=10000, default="Not exist")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    isInWork = models.BooleanField(default=False)
    file = models.FileField(null=True, upload_to='files/', blank=True)
    creationTime = models.DateTimeField(auto_now=False, auto_now_add=True)
