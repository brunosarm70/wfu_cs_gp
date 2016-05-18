from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Tournament, Game, Player, Code, Tournament_Status, Competitor, Match, Score, WebSiteInfo
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Max, Sum


# erase this later
def runtournament(request, pk):
    Competitor.objects.all().delete()
    Match.objects.all().delete()
    Score.objects.all().delete()
    t = Tournament.objects.get(pk = pk)
    t.run_tournament()
    return HttpResponseRedirect('/admin/gp/')


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
    try:
        open_status = Tournament_Status.objects.get(name = 'Open')
    except:
        open_status = None
    tournaments = Tournament.objects.filter(status = open_status).order_by('datetime')[:3]
    
    # query the information of the home page
    info = WebSiteInfo.objects.all()[0]
    
    # home template, for logged and anonymous users
    return render(request, 'gp/home.html', {'tournaments': tournaments, 'info': info})




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





def upcoming_queries(request):
    # query all the unstarted tournaments ordered by date
    try:
        status = Tournament_Status.objects.get(name = "Open")
    except:
        status = None
    tournaments = Tournament.objects.filter(status = status).order_by('datetime')

    
    # query the tournaments where the player is already registered
    registered_tournaments = []
    if(request.user.is_authenticated()):
        pPlayer = Player.objects.get(user=request.user)
        print(pPlayer)
        registered_codes = Code.objects.filter(player = pPlayer)
        for code in registered_codes:
            registered_tournaments.append(code.tournament)
            
    parameters = [tournaments, registered_tournaments]
    
    return parameters



# Upcoming tournaments view ('/tournaments/upcoming/')
def upcoming(request):    
    
    # call the necessary queries
    queries = upcoming_queries(request)
    
    # set the flags at 0 because there are no messages to display
    error = 0
    success = 0
    msg = ""
    
    # template to display all the upcoming tournaments
    return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg, 'error': error, 'success': success})



# Finished tournaments view ('/tournaments/finished/')
def finished(request): 
    # call the necessary queries
    tournaments = Tournament.objects.filter(status__name = 'Finished')
    
    # template to display all the finished tournaments
    return render(request, 'gp/finished.html', {'tournaments': tournaments})



def view_results(request):
    
    league_table = []
    matches_per_round = []
    
    if request.method == 'POST':
        # get the primary key of the tournament from the request
        tournament_pk = request.POST.get('tournament', '')
        
        # verify if the tournament exist
        if Tournament.objects.filter(pk = tournament_pk).count() > 0:
            # get the specific tournament
            tournament = Tournament.objects.get(pk = tournament_pk)
            rounds = tournament.matches.all().aggregate(Max('round_number'))['round_number__max']
            
            if(tournament.tournament_type.name == "Bracket"):
                for r in range(1, rounds + 1):
                    matches = [m.competitors.all() for m in Match.objects.filter(tournament = tournament, round_number = r)]
                    for m in range (0, len(matches)):
                        matches[m] = [ m+1 , matches[m] ] 
                    matches_plus_round = [r, matches]
                    matches_per_round.append(matches_plus_round)
                
            elif(tournament.tournament_type.name == "League"):
                players = []
                participants = Code.objects.filter(tournament = tournament)
                for participant in participants:
                    players.append(participant.player)
                
                for player in players:
                    player_data = []
                    player_data.append(player)
                    player_data.append(tournament.matches.filter(winner = player).count())
                    player_data.append(tournament.matches.filter(competitors__player = player).exclude(winner = player).count())
                    my_competitors = [m.competitors.filter(player = player)[0] for m in tournament.matches.filter(competitors__player = player)]
                    total_score = 0 
                    for competitor in my_competitors:
                        total_score += competitor.scores.all().aggregate(Sum('score'))['score__sum']
                    player_data.append(total_score)
                    league_table.append(player_data)
                    
                league_table.sort(key=lambda x:x[3], reverse=True)
                league_table.sort(key=lambda x:x[1], reverse=True)
            
                for i in range (0, len(league_table)):
                    league_table[i] = [i+1] + league_table[i]
                
                matches_per_round = [m.competitors.all() for m in Match.objects.filter(tournament = tournament)] 
                for m in range (0, len(matches_per_round)):
                    matches_per_round[m] = [ m+1 , matches_per_round[m] ]
                
                
            
            if(tournament != None):
                return render(request, 'gp/results.html', {'tournament': tournament, 'rounds': rounds, 'table': league_table, 'matches_per_round': matches_per_round})
            else:
                return HttpResponseRedirect('/tournaments/finished/')
        else:
            return HttpResponseRedirect('/tournaments/finished/')
    return HttpResponseRedirect('/tournaments/finished/')





# Profile view ('/myprofile/')
def profile(request):
    # if the user is not authenticated they will be redirected to the login page
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    
    # query the player asociated to the user
    player = Player.objects.get(user=request.user)
    
    wins = Match.objects.filter(winner = player).count()
    won_tournaments = Tournament.objects.filter(winner = player).count()
    losses =  Match.objects.filter(competitors__player = player).exclude(winner = player).count()
    lost_tournaments = Code.objects.filter(player = player, tournament__status__name = 'Finished').count() - won_tournaments
    
    
    # template to display player details
    return render(request, 'gp/profile.html', {'player': player, 'wins' : wins, 'won_tournaments' : won_tournaments, 'losses' : losses, 'lost_tournaments' : lost_tournaments})






# Login view ('/login/')
def login_view(request):
    there_is_an_error = 0
    error_title = "Login failed: "
    error_body = ""
    
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
            there_is_an_error = 1
            error_body += "The username and password don't match. Please try again."
            return render(request, 'registration/login.html' , {'error_title': error_title, 'errors': there_is_an_error, 'error_body' : error_body})
    
    # if something goes wrong, the login page will reload
    return render(request, 'registration/login.html' , {'redirect_to': next, 'error_title': error_title, 'errors': there_is_an_error, 'error_body' : error_body})
    
    
    
    
    
# Logout view ('/logout/')    
def logout_view(request):
    # logout the user
    logout(request)
    
    # redirect to the home page
    return HttpResponseRedirect(settings.LOGIN_URL)





def register_in_a_tournament2(request, pk):
    msg = ""
    
    # query the specific tournament
    tournament = get_object_or_404(Tournament, pk=pk)
    player = Player.objects.get(user=request.user)
    
    code = Code.objects.filter(player = player, tournament = tournament).count()
    if code > 0:
        msg = "El jugador ya se ha registrado en el torneo."
        queries = upcoming_queries(request)
        return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg})
    
    # if the tournament exist
    if not tournament==None:
        # if the tournament status is equals to "Unstarted"
        if tournament.status == "Unstarted": 
            # player get register in the tournament
            new_code = Code.objects.create(tournament = tournament, player = player, url = None)
            new_code.save()
            
            msg = "Player registered in " + str(tournament)
            queries = upcoming_queries(request)
            return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg})
    
    queries = upcoming_queries(request)
    return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg})




def register_in_a_tournament(request):
    # initialize the message to be displayed in case of error or success
    msg = ""
    # set the flags at 0
    error = 0
    success = 0
    
    if request.method == 'POST':
        # get the parameters (the code and the tournament id)
        pk = request.POST.get('tournament', '')
        
        if len(request.FILES) == 0:
            # set the error flag at 1
            error = 1
            msg += "There wasn't any files attached."
        else:
        
            url = request.FILES['docfile']

            # query the specific tournament and the player doing the registration
            tournament = get_object_or_404(Tournament, pk=pk)
            player = Player.objects.get(user=request.user)

            # verify that doesn't exist a code for that tournament related to that player
            code = Code.objects.filter(player = player, tournament = tournament).count()
            
            try:
                open_status = Tournament_Status.objects.get(name = 'Open')
            except:
                open_status = None
            
            if(tournament.datetime <= timezone.now() or tournament.status != open_status):
                error = 1
                msg += "The registration period of the tournament is already closed."
            else:
                if code > 0:
                    # set the error flag at 1
                    error = 1
                    msg += "The player is already registered in the tournament."
                else:

                    # verify that the file has a .py extension
                    if url.content_type != 'text/x-python-script':
                        msg += "The uploaded file should has the .py extension."
                        # set the error flag at 1
                        error = 1
                    else:
                        # if the tournament exist
                        if not tournament==None:
                            
                            if(tournament.n_registered_players < tournament.maxPlayers):
                            
                                # player get register in the tournament
                                new_code = Code.objects.create(tournament = tournament, player = player, url = url)
                                new_code.save()
                                tournament.n_registered_players += 1
                                tournament.save()

                                msg += "Player registered in " + str(tournament) + "."
                                # set 
                                success = 1
                                queries = upcoming_queries(request)
                                return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg, 'error': error, 'success': success})
                            else:
                                error = 1
                                msg += "The tournament is full."
                        else:
                            error = 1
                            msg += "The tournament doesn't exist."
            
            
    # if there are no messages to display, redirect to /tournaments/upcoming
    if(error == 0 and success == 0):
        return HttpResponseRedirect('/tournaments/upcoming/')
    
    
    queries = upcoming_queries(request)
    return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg, 'error': error, 'success': success})




def change_code(request):
    # initialize the message to be displayed in case of error or success
    msg = ""
    # set the flags at 0
    error = 0
    success = 0
    
    if request.method == 'POST':
        # get the parameters (the code and the tournament id)
        pk = request.POST.get('tournament', '')
        
        if len(request.FILES) == 0:
            msg += "There wasn't any files attached."
            
            # set the error flag at 1
            error = 1
            queries = upcoming_queries(request)
            return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg, 'error': error, 'success': success})

        
        url = request.FILES['docfile']

        # query the specific tournament and the player doing the registration
        tournament = get_object_or_404(Tournament, pk=pk)
        player = Player.objects.get(user=request.user)
        
        try:
            closed_status = Tournament_Status.objects.get(name = "Open")
            open_status = Tournament_Status.objects.get(name = "Closed")
        except:
            closed_status = None
            open_status = None
            
        if(tournament.datetime <= timezone.now() or (tournament.status != open_status and tournament.status != closed_status)):
            error = 1
            msg += "The period to change the code is already closed."
            queries = upcoming_queries(request)
            return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg, 'error': error, 'success': success})
    
    
        # verify that doesn't exist a code for that tournament related to that player
        code = Code.objects.filter(player = player, tournament = tournament).count()
        if code == 0:
            msg += "The player hasn't registered any code in the tournament."
            
            # set the error flag at 1
            error = 1
            queries = upcoming_queries(request)
            return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg, 'error': error, 'success': success})
    
        # verify that the file has a .py extension
        if url.content_type != 'text/x-python-script':
            msg += "The uploaded file should has the .py extension."
            # set the error flag at 1
            error = 1
            queries = upcoming_queries(request)
            return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg, 'error': error, 'success': success})
        
        
        # if the tournament exist
        if not tournament==None:
            # if the tournament status is equals to "Open"
            open_status = Tournament_Status.objects.get(name = "Open")
            closed_status = Tournament_Status.objects.get(name = "Closed")
            if tournament.status == open_status or tournament_status == closed_status: 
                # changes the code of the player in the tournament
                player_code = Code.objects.get(tournament = tournament, player = player)
                player_code.url = url
                player_code.save()

                msg += "Player changed successfully the code in " + str(tournament) + "."
                # set 
                success = 1
                queries = upcoming_queries(request)
                return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg, 'error': error, 'success': success})
            else:
                error = 1
                msg += "This tournament doesn't allow any more code changes."
        else:
            error = 1
            msg += "The tournament doesn't exist."
            
            
    # if there are no messages to display, redirect to /tournaments/upcoming
    if(error == 0 and success == 0):
        return HttpResponseRedirect('/tournaments/upcoming/')
    
    
    queries = upcoming_queries(request)
    return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg, 'error': error, 'success': success})



def unregister(request):
    # set the flags at 0
    success = 0
    error = 0
    msg = "There's been an error unregistering the player."
    
    if request.method == 'POST':
        # get the primary key of the tournament from the request
        tournament_pk = request.POST.get('tournament', '')
        
        # verify if the player and the tournament exist
        if Player.objects.filter(user = request.user).count() > 0 and Tournament.objects.filter(pk = tournament_pk).count() > 0:
            # get the specific player and tournament
            player = Player.objects.get(user = request.user)
            tournament = Tournament.objects.get(pk = tournament_pk)
            
            try:
                open_status = Tournament_Status.objects.get(name = 'Open')
            except:
                open_status = None
            if(tournament.datetime <= timezone.now() or tournament.status != open_status):
                error = 1
                msg = "The registration period for this tournament has closed."
            else:
                # verify that the player has a registered code for the tournament
                codes = Code.objects.filter(tournament = tournament, player = player).count()
                if(codes > 0):
                    # delete the code from the database
                    Code.objects.get(tournament = tournament, player = player).delete()
                    tournament.n_registered_players -= 1
                    tournament.save()

                    # set the success flag at 1
                    success = 1
                    msg = "Player unregistered from " + str(tournament) + " successfully."

                    queries = upcoming_queries(request)
                    return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg, 'error': error, 'success': success})
                else:
                    # set the error flag at 1
                    error = 1
                    msg = "The player wasn't registered for this tournament."
        
    
    if not error and not success:
        return HttpResponseRedirect('/tournaments/upcoming/')
    
    queries = upcoming_queries(request)
    return render(request, 'gp/upcoming.html', {'tournaments': queries[0], 'registered_t' : queries[1], 'message': msg, 'error': error, 'success': success})


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
    
    there_is_an_error = 0
    error_title = "Registration failed: "
    error_body = ""
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
        
    if(len(errors) > 0):
        there_is_an_error = 1
        password_error = False
        for error in errors:
            if(error == 'username'):
                error_body += 'The username is empty or is already being used. '
            elif(error == 'first_name'):
                error_body += 'The first name field is empty. '
            elif(error == 'last_name'):
                error_body += 'The last name field is empty. '
            elif(error == 'email'):
                error_body += 'The email is empty or is already being used. '
            elif((error == 'password1' or error == 'password2') and not password_error):
                error_body += "The password fields don't match. "
                password_error = True
                
    return render(request, "registration/login.html", {'form': form, 'error_title': error_title, 'errors': there_is_an_error, 'error_body': error_body })






#{% url 'django.contrib.auth.views.logout' %}
#{% url 'django.contrib.auth.views.login' %}