from .forms import LoginForm

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def index(request):
    context = {}
    return render(request, 'home/index.html', context)

def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request)
        if (form.is_valid()):
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
    else:
        form = LoginForm()
        context = {'form': form}
        return render(request, 'home/log_in.html', context)

def log_out(request):
    logout(request)
    return redirect('index')

def homepage(request):
    context = {}
    return render(request, 'home/homepage.html', context)

def designs(request):
    context = {}
    return render(request, 'home/designs.html', context)

def team(request):
    context = {}
    return render(request, 'home/team.html', context)

def dataEntry(request):
    context = {}
    return render(request, 'home/dataEntry.html', context)

def launches(request):
    context = {}
    return render(request, 'home/launches.html', context)
