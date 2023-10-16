from django.urls import include, path
from .import views

urlpatterns = [
 path("" , views.index, name="index"),
 path("register/" , views.register, name="register"),
 path("update/" , views.update, name="update"),
 
 path("login/" , views.signin, name="login"),
 path("logout/" , views.signout, name="logout"),
 path("suggestions/" , views.suggestions, name="suggestions"),
 
 path("send-request/" , views.sendFriendRequest , name="send-request"),
 path("friend-request/" , views.friend_request , name="friend-request"),
 path("accept-request/" , views.accept_friend_request , name="accept-request"),
 
 
 
]
