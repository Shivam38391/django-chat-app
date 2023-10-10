from django.shortcuts import redirect, render

from .forms import UserForm
from django.contrib.auth import authenticate, login, logout

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