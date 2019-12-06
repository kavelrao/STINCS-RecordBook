from django.shortcuts import render

# Create your views here.
def index(request):
    context = {}
    return render(request, 'home/index.html', context)

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
