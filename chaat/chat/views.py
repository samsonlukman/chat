from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from .models import User, ChatMessage
from django.shortcuts import redirect, render, get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm




def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    messages = ChatMessage.objects.all().order_by('-timestamp')[:30]  # Fetch the latest 10 messages (you can adjust the number)

    return render(request, 'chat/index.html', {'messages': messages})


def get_messages(request):
    messages = ChatMessage.objects.all()
    data = [{'message': message.message} for message in messages]
    return JsonResponse(data, safe=False)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chat/login.html", {
            "message": "Invalid username and/or password"
        })

    else:
        return render(request, "chat/login.html")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'chat/register.html', {'form': form})
