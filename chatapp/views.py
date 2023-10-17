import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import FriendRequest, Profile, Notification
from .forms import ProfileForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="login")
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


@login_required(login_url="login")
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


@login_required(login_url="login")
def suggestions(request):
    all_user = get_user_model()
    user = request.user
    profile = Profile.objects.get(user=user)
    profile_friends = profile.friends.all()
    suggested_friends = all_user.objects.exclude(profile__friends__in =profile_friends ).exclude(profiles= profile)
    
    friend_requests = FriendRequest.objects.filter(receiver__in = suggested_friends , sender = request.user)
    
    context = {"s_friends": suggested_friends , "f_requests": friend_requests}
    return render(request,"chatapp/suggestions.html" ,context)

@login_required(login_url="login")
def sendFriendRequest(request):
    
    # data comming from the front end
    data = json.loads(request.body)
    user = get_user_model() # we are using django default user model , this funxction gives us the activer user model u dont need to import the User Mode
    
    receiver = user.objects.get(id = data)
    print(data)# id of users
    friend_request = FriendRequest.objects.create(sender = request.user, receiver= receiver)
    return JsonResponse("it is runing ", safe= False)




@login_required(login_url="login")
def friend_request(request):
    user = request.user
    friend_requests = FriendRequest.objects.filter(receiver= user)
    context = {"f_requests": friend_requests}
    return render(request, "chatapp/friend_request.html", context)

@login_required(login_url="login")
def accept_friend_request(request):
    id = json.loads(request.body)
    user_id = id
    user= get_user_model()
    n_user = user.objects.get(id = user_id)
    profile = Profile.objects.get(user_id = request.user.id)
    profile2 = Profile.objects.get(user_id = user_id)
    f_request = FriendRequest.objects.get(sender= n_user, receiver = request.user)
    msg = None
    
    if profile:
        
        if profile.friends.filter(id = user_id).exists():
            profile.friends.remove(n_user)
            msg = "No"
            
        else:
            profile.friends.add(n_user)
            f_request.delete()
            Notification.objects.create(sender = request.user, receiver= n_user, 
                                        description = f"Hi , {request.user.username} accepted your request.")
            
            
            msg = "Yes"
    
    
    if profile2:
        if profile2.friends.filter(id= request.user.id).exists():
            profile2.friends.remove(request.user)
            
        else:
            profile2.friends.add(request.user)
    
    
    return JsonResponse(msg, safe=False)