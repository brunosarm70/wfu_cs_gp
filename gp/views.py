from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Tournament, Game, Player
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def home2(request):
    tournaments = Tournament.objects.all().order_by('datetime')
    return render(request, 'gp/index.html', {'tournaments': tournaments})


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    
    return render(request, 'registration/login.html')
    #return HttpResponseRedirect('/login/')
    
def home(request):
    tournaments = Tournament.objects.all().order_by('datetime')[:3]
    return render(request, 'gp/home.html', {'tournaments': tournaments})

def games(request):
    games = Game.objects.all()
    return render(request, 'gp/games.html', {'games': games})

def upcoming(request):
    tournaments = Tournament.objects.filter(status='Unstarted').order_by('datetime')
    return render(request, 'gp/upcoming.html', {'tournaments': tournaments})

def detailed_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'gp/game.html', {'game': game})


def login_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    
    next = request.GET.get('next', '/home/')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # Correct password, and the user is marked "active"
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(next)
            else:
                # Show an error page
                return HttpResponse("Inactive User.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
            
    return render(request, 'registration/login.html' , {'redirect_to': next})
    
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(settings.LOGIN_URL)



def register_view(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    
    errors = []
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        pEmail = request.POST.get('email', '')
            
        if(first_name == ""):
            errors.append("first_name")
            
        if(last_name == ""):
            errors.append("last_name")
                
        users_email = User.objects.filter(email=pEmail).count()
        if(users_email > 0 or pEmail==""):
            errors.append('email')

        if form.is_valid() and (len(errors) == 0):
            # There's no errors on the inputs
            new_user = form.save()
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.email = pEmail
            new_user.save()
            
            player = Player.objects.create()
            player.user = new_user
            player.save()
            
            user = authenticate(username = new_user.username, password = request.POST.get('password1', ''))
            
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/home/")
            
            return HttpResponseRedirect(settings.LOGIN_URL)
            
            
        else:
            #form.add_error('mi_error','es una prueba')
            for e in form.errors:
                errors.append(e)
    else:
        form = UserCreationForm()
    return render(request, "registration/login.html", {'form': form, 'errors': errors })



#{% url 'django.contrib.auth.views.logout' %}
#{% url 'django.contrib.auth.views.login' %}