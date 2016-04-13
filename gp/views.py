from django.shortcuts import render
from .models import Tournament, Game

# Create your views here.

def home2(request):
    tournaments = Tournament.objects.all().order_by('datetime')
    return render(request, 'gp/index.html', {'tournaments': tournaments})


def index(request):
    return render(request, 'gp/index.html')

def home(request):
    tournaments = Tournament.objects.all().order_by('datetime')[:3]
    return render(request, 'gp/home.html', {'tournaments': tournaments})

def games(request):
    games = Game.objects.all()
    return render(request, 'gp/games.html', {'games': games})