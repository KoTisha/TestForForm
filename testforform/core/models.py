from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SubmitUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastSubmitDate = models.DateTimeField(blank=True, null=True)

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=350, default="Not exist")
    message = models.TextField(max_length=10000, default="Not exist")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    isInWork = models.BooleanField(default=False)
    file = models.FileField(null=True, upload_to='files/', blank=True)
    creationTime = models.DateTimeField(auto_now=False, auto_now_add=True)


@receiver(post_save, sender=User)
def create_submituser(sender, instance, created, **kwargs):
    if created:
        SubmitUser.objects.create(user=instance)
