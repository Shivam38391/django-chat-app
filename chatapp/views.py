from django.shortcuts import redirect, render
from .models import Profile
from .forms import ProfileForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

# Create your views here.

def index(request):
    return render(request, "chatapp/index.html")


def register(request):
    # if user logged in, cant access to register page
    if request.user.is_authenticated:
        return redirect("index")
    form = UserForm()
    
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            
            #login user after registration
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
    
            return redirect("index")
    
    context = {"form": form}
    return render(request, "chatapp/register.html", context)




def signin(request):
    if request.user.is_authenticated:
        return redirect("index")
    error_msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            error_msg = "Invalid username or password"

    context = {"msg": error_msg}
    return render(request, "chatapp/login.html" , context)



def signout(request):
    logout(request)
    return redirect('login')



def update(request):
    if not request.user.is_authenticated:
        return redirect("login")
    user = request.user
    # username = request.user.username
    profile = Profile.objects.get(user=user)
    form = ProfileForm(instance = profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("update")
    context = {"form": form}
    
    return render(request, "chatapp/update-profile.html", context )



def suggestions(request):
    all_user = get_user_model()
    user = request.user
    
    profile = Profile.objects.get(user=user)
    profile_friends = profile.friends.all()
    suggested_friends = all_user.objects.exclude(profile__friends__in =profile_friends ).exclude(profiles= profile)
    context = {"s_friends": suggested_friends}
    return render(request,"chatapp/suggestions.html" ,context)