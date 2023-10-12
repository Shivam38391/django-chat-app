from django.urls import include, path
from .import views

urlpatterns = [
 path("" , views.index, name="index"),
 path("register/" , views.register, name="register"),
 path("update/" , views.update, name="update"),
 
 path("login/" , views.signin, name="login"),
 path("logout/" , views.signout, name="logout"),
 
 
 
]
