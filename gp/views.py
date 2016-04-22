from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Tournament, Game, Player, Code
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

# Index view ('/')
def index(request):
    # if the user is already logged, is not permitted to see this page
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')

    # redirect to login and registration template
    return render(request, 'registration/login.html')




    
# Home view ('/home/')
def home(request):
    # query the 3 closer upcoming tournaments
    tournaments = Tournament.objects.all().order_by('datetime')[:3]
    
    # home template, for logged and anonymous users
    return render(request, 'gp/home.html', {'tournaments': tournaments})




# Game view ('/games/')
def games(request):
    # query all the games
    games = Game.objects.all()
    
    # template to display the games
    return render(request, 'gp/games.html', {'games': games})




# Detailed game view ('/game/<pk>/') <pk> : primary key
def detailed_game(request, pk):
    # query the specific game
    game = get_object_or_404(Game, pk=pk)
    
    # template to display an specific game
    return render(request, 'gp/game.html', {'game': game})





# Upcoming tournaments view ('/tournaments/upcoming/')
def upcoming(request):
    # query all the unstarted tournaments ordered by date
    tournaments = Tournament.objects.filter(status='Unstarted').order_by('datetime')
    
    # query the tournaments where the player is already registered
    registered_tournaments = []
    if(request.user.is_authenticated()):
        pPlayer = Player.objects.get(user=request.user)
        registered_codes = Code.objects.filter(player = pPlayer)
        for code in registered_codes:
            registered_tournaments.append(code.tournament)
    
    # template to display all the upcoming tournaments
    return render(request, 'gp/upcoming.html', {'tournaments': tournaments, 'registered_t' : registered_tournaments})





# Profile view ('/myprofile/')
def profile(request):
    # if the user is not authenticated they will be redirected to the login page
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    # query the player asociated to the user
    player = Player.objects.get(user=request.user)
    
    # template to display player details
    return render(request, 'gp/profile.html', {'player': player})





# Login view ('/login/')
def login_view(request):
    # if the user is already authenticated they will be redirected to the home page
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    
    # establish the home page as the success page
    next = request.GET.get('next', '/home/')
    
    if request.method == 'POST':
        # retrieve the username and password provided by the user
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        # verify is the password and username match with the ones in the database
        user = authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_active:
                # log the user in the system
                login(request, user)
                
                # redirect to the home page
                return HttpResponseRedirect(next)
            else:
                # Show an error page
                return HttpResponse("Inactive User.")
            
        # if the username or the password don't match, the user will be redirect to login page
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    
    # if something goes wrong, the login page will reload
    return render(request, 'registration/login.html' , {'redirect_to': next})
    
    
    
    
    
# Logout view ('/logout/')    
def logout_view(request):
    # logout the user
    logout(request)
    
    # redirect to the home page
    return HttpResponseRedirect(settings.LOGIN_URL)





def register_in_a_tournament(request):
    return render(request, 'gp/upcoming.html')





def edit_profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    errors = []
    if request.method == 'POST':
        
        pUsername = request.POST.get('username', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        pEmail = request.POST.get('email', '')
            
        if(first_name == ""):
            errors.append("first_name")
            
        if(last_name == ""):
            errors.append("last_name")
        
        # Verify if the username is unique
        users_username = User.objects.filter(username=pUsername).count()
        if(users_username > 0 or pUsername==""):
            if(not (users_username == 1 and request.user.username == pUsername)):
                errors.append('username')
        
        # Verify if the email is unique
        users_email = User.objects.filter(email=pEmail).count()
        if(users_email > 0 or pEmail==""):
            if(not (users_email == 1 and request.user.email == pEmail)):
                errors.append('email')

        if(len(errors) == 0):
            # There's no errors on the inputs
            request.user.username = pUsername
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = pEmail
            request.user.save()
            
            return HttpResponseRedirect('/myprofile/')
            
            
    player = Player.objects.get(user=request.user)
    
    return render(request, 'gp/edit_profile.html', {'player': player, 'errors': errors})
    

    
    
    
    
    
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