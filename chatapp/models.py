from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name="profiles" )
    username = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="img", blank=True , null=True)
    friends = models.ManyToManyField(User, blank=True, null=True)
    

    def __str__(self):
        return self.username


class FriendRequest(models.Model):
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE , related_name="sent_requests") # sender is the logged in user
    receiver = models.ForeignKey(User, on_delete=models.CASCADE , related_name="received_request") # receiver is the that clicked upon
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} sents a request to {self.receiver.username}"
