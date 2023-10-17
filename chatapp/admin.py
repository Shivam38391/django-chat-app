from django.contrib import admin
from .models import Notification, Profile , FriendRequest
# Register your models here.
admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(Notification)

