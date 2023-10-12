from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Profile


class UserForm(UserCreationForm):
    username = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control', "placeholder": "enter username"}))
    email = forms.EmailField(widget= forms.TextInput(attrs={'class': 'form-control', "placeholder": "enter Email"}))
    password1 = forms.CharField(widget= forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "enter password"}))
    password2 = forms.CharField(widget= forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "confirm password"}))
    
    
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']




class ProfileForm(forms.ModelForm):
    """Form definition for Profile."""
    username = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control', "placeholder": "enter username"}))
    first_name = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control', "placeholder": "Update first name"}))
    last_name = forms.CharField(widget= forms.TextInput(attrs={'class': 'form-control', "placeholder": "Update last name"}))
    
    
    class Meta:
        """Meta definition for Profileform."""

        model = Profile
        fields =["username", "first_name", "last_name", "profile_picture", ]
