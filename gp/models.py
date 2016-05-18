from django.db import models
from django.utils import timezone
import time
from datetime import datetime, timedelta
from gp.tasks import call_run_tournament
import itertools
from random import shuffle
import math


# Models

class Country(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name
    

class University(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=4)
    country = models.ForeignKey(Country, default = 0)
    
    def __str__(self):
        return self.name
    
    
class Player(models.Model):
    user = models.ForeignKey('auth.User', default=0)
    country = models.ForeignKey(Country, default = 0)
    university = models.ForeignKey(University, default = 0)
    
    def __str__(self):
        return self.user.get_full_name()
    
    
class Game(models.Model):
    name = models.CharField(max_length=100)
    minPlayers = models.IntegerField()
    maxPlayers = models.IntegerField()
    description = models.TextField()
    rules = models.TextField(null = True)
    controller = models.FileField(upload_to="./controllers/", blank=True, null=True)
    function_player_name = models.CharField(max_length=100, default = "function_name")
    
    def __str__(self):
        return self.name
    
    
# Status: Unpublished, Open, Closed, Running, Finished
class Tournament_Status(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
# Types: Bracket, League
class Tournament_Type(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
    
class Score(models.Model):
    score = models.IntegerField(default = 0)
    game_number = models.IntegerField(default = 0)
    
    def __str__(self):
        return str(self.score) + " in game #" + str(self.game_number)


class Competitor(models.Model):
    player = models.ForeignKey(Player, default = 0)
    won_games = models.IntegerField(default = 0)
    scores = models.ManyToManyField(Score, blank = True)
    match_played = models.ForeignKey('Match', default = 0)
    tournament = models.ForeignKey('Tournament', default = 0)
    datetime = models.DateTimeField(null = True, default = None)
    
    def __str__(self):
        return "Competitor " + str(self.player) + " in " + str(self.tournament)
    
    
class Match(models.Model):
    competitors = models.ManyToManyField(Competitor, blank = True)
    winner = models.ForeignKey(Player, null = True)
    round_number = models.IntegerField(default = 0)
    datetime = models.DateTimeField(null = True, default = None)
    
    def __str__(self):
        return "Match of round #" + str(self.round_number)
    
    def is_there_a_winner(self, games_to_win_the_match):
        for competitor in self.competitors.all():
            if competitor.won_games == games_to_win_the_match:
                return True
        return False
    
    def run_match(self, tournament):
        # creates a list of the players participating in the match
        players = []
        for competitor in self.competitors.all():
            players.append(competitor.player)
        
        # creates a list of the player codes
        codes = []
        for player in players:
            codes.append(Code.objects.get(tournament = tournament, player = player))
    
        # takes the game controller and puts it in a variable
        tournament.game.controller.open()
        controller_code = tournament.game.controller.read()
        exec(controller_code)
        tournament.game.controller.close()
        controller_func = locals()['controller']
        
        # if there's only one player, it wins automatically
        if(len(codes) == 1):
            for c in self.competitors.all():
                self.winner = c.player
                break
            self.save()
            return
        
        
        game_number = 1     
        while not self.is_there_a_winner(tournament.games_to_win_the_match):
            scores = controller_func(codes, tournament)
            
            scores_list = []
            winners_indexes = [] 
            for score in scores:
                scores_list.append(score[0])
            
            if scores_list != []:
                winning_score = max(scores_list)
                for i in range(0, len(scores_list)):
                    if scores_list[i] == winning_score:
                        winners_indexes.append(i)
            
            for i in range (0, len(scores)):
                player_score = scores[i]
                aux_competitor = self.competitors.get(player = player_score[1])
                aux_competitor.scores.add(Score.objects.create(score = player_score[0], game_number = game_number))
                if i in winners_indexes:
                    aux_competitor.won_games += 1
                aux_competitor.save()
            
            game_number += 1   

        # select any winner
        winners = []
        for competitor in self.competitors.all():
            if competitor.won_games == tournament.games_to_win_the_match:
                winners.append(competitor.player)
                
        self.winner = winners[0]
        self.save()
    
    
    
    
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    minPlayers = models.IntegerField(default = 2)
    maxPlayers = models.IntegerField(default = 100)
    players_per_match = models.IntegerField(default = 2)
    games_to_win_the_match = models.IntegerField(default = 1)
    status = models.ForeignKey(Tournament_Status, default = 0)
    game = models.ForeignKey(Game, default = 0)
    tournament_type = models.ForeignKey(Tournament_Type, default = 0)
    matches = models.ManyToManyField(Match, blank = True)
    datetime = models.DateTimeField(null = True, default = None)
    last_datetime = models.DateTimeField(null = True, default = None)
    description = models.TextField(null = True)
    winner = models.ForeignKey(Player, null = True, blank = True)
    n_registered_players = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.name
    
    # simulate the matches of the tournament of an specific round
    def execute_matches(self, round_number):
        for match in self.matches.all():
            # run the matches of the specified round
            if match.round_number == round_number:
                match.run_match(self)
    
    def set_league_winner(self, participants):
        # creates a list of players and another one for count the wins of each
        players = []
        wins = []
        scores_for = []
        for participant in participants:
            players.append(participant.player)
            wins.append(0)
            scores_for.append(0)
            
        for p in range(0, len(players)):
            player = players[p]
            my_competitors = Competitor.objects.filter(player = player, tournament = self)
            for my_competitor in my_competitors:
                for score in my_competitor.scores.all():
                    scores_for[p] += score.score
        
        for match in self.matches.all():
            if match.winner in players:
                wins[players.index(match.winner)] += 1
        
        
        max_wins = max(wins)
        winners = []
        
        for i in range(0, len(wins)):
            if max_wins == wins[i]:
                winners.append(i)
            print(str(players[i]) + ": W: " + str(wins[i]) + " SF: " + str(scores_for[i]))
            
        print(winners)
        print(wins)
        
        if len(winners) > 1:
            scores_for_tiebreaker = []
            for w in winners:
                scores_for_tiebreaker.append(scores_for[w])
            
            winner = scores_for_tiebreaker.index(max(scores_for_tiebreaker))
            self.winner = players[winners[winner]]
        else:
            print(players[winners[0]])
            self.winner = players[winners[0]]
        self.save()
    
    def run_tournament_league(self, participants):
        # create a list of every single combination of n players possible between all the tournament participants 
        # n being the players per match specified at the tournament creation
        combinations = list(itertools.combinations(participants, self.players_per_match))

        print("AQUI EMPIEZA===============================")
        print(len(combinations))
        # create a match for every single combination
        for combination in combinations:
            # create match (always round #1 becuase is a league)
            match = Match.objects.create(round_number = 1, datetime = timezone.now())
            # for every player in the "combination" it creates a competitor
            print(combination)
            if(len(combination) > self.players_per_match):
                print("ALGO ANDA MAL AQUI ===============================")
            for code in combination:
                # create competitor
                match.competitors.add(Competitor.objects.create(player = code.player, tournament = self, match_played = match, datetime = timezone.now()))
            # add the match to the list of matches of the tournament
            self.matches.add(match)
        # save the tournament in the database
        print("AQUI TERMINAA===============================")
        self.save()
        
        # execute games of the round #1 (in a league is the only round) 
        self.execute_matches(1)
        
        # set winners
        self.set_league_winner(participants)
        
        
    # create the first round of matches of the bracket tournament and then returns the amount of rounds needed to complete it
    def set_first_round(self, participants):
        # take the list of participants and shuffles it
        shuffled_participants = list(participants)
        shuffle(shuffled_participants)
        
        # calculate the rounds needed, the total players neeeded and the matches needed (brackets_needed) in this round
        amount_of_players = len(shuffled_participants) 
        rounds_needed = math.ceil(math.log(amount_of_players, self.players_per_match))
        players_needed = math.pow(self.players_per_match, rounds_needed) 
        brackets_needed = (int) (players_needed / self.players_per_match)
        
        # create an empty list for every match needed
        matches = []
        for bracket in range(0, brackets_needed):
            matches.append([])
        
        # this iterator will help 
        brackets_needed_iterator = 0
        for player in shuffled_participants:
            matches[brackets_needed_iterator].append(player)
            brackets_needed_iterator += 1
            if brackets_needed_iterator == brackets_needed:
                brackets_needed_iterator = 0
        
        for match in matches:
            aux_match = Match.objects.create(round_number = 1, datetime = timezone.now())
            for code in match:
                aux_match.competitors.add(Competitor.objects.create(player = code.player, tournament = self, match_played = aux_match))
            self.matches.add(aux_match)
            
        return rounds_needed
        
    
    def set_next_round(self, previous_round):
        # create a list of players who won their matches in the previous round
        winners = []
        for match in self.matches.all():
            if match.round_number == previous_round:
                winners.append(match.winner)
        
        # player_iterator will help to keep track of the amount of players of the matches being created, not greater the players per match
        player_iterator = 0
        aux_match = None
        for winner in winners:
            # creates a new match
            if player_iterator == 0:
                # the round should be 1 greater than the previous
                new_round = previous_round + 1
                aux_match = Match.objects.create(round_number = new_round, datetime = timezone.now())
                
            # creates a new competitor using a winner and add it to the list of competitors of the match created
            aux_match.competitors.add(Competitor.objects.create(player = winner, tournament = self, match_played = aux_match))

            # increase the iterator to see if we added enough players to the match
            player_iterator += 1
            if player_iterator == self.players_per_match:
                # if there are enough players in the match, we add the match to the list of matches of the tournament
                player_iterator = 0
                self.matches.add(aux_match)
    
        
    def run_tournament_bracket(self, participants):
        # set_first_round create the initial bracket according to the registered players 
        # of the tournament and the specified players_per_match
        # the function returns the required amount of rounds to run the tournament 
        rounds_needed = self.set_first_round(participants)
        
        # execute games round by round
        for round_number in range(1, rounds_needed + 1):
            self.execute_matches(round_number)
            # if the round is not the last one, a function to create the next round is called and it creates the matches
            if(round_number != rounds_needed):
                self.set_next_round(round_number)
    
        # set winner (in a bracket the winner is the winner of the only game of the last round)
        self.winner = self.matches.get(round_number = rounds_needed).winner 
        self.save()
        
    
    def run_tournament(self):
        if(self.n_registered_players < self.minPlayers):
            self.datetime += timedelta(0, 0, 0, 0, 7) # plus 7 minutes
            self.save()
            return
        
        
        # set the tournament status at "running"
        self.status = Tournament_Status.objects.get(name = 'Running')
        self.save()
        
        # Get the participants of the tournament
        participants = Code.objects.filter(tournament = self)
        
        # Run the tournament depending of the type
        if self.tournament_type.name == "Bracket":
            self.run_tournament_bracket(participants)
            
        if self.tournament_type.name == "League":
            self.run_tournament_league(participants)
       
        self.status = Tournament_Status.objects.get(name = 'Finished')
        self.save()



class Code(models.Model):
    url = models.FileField(upload_to="./codes/", blank=True, null=True)
    player = models.ForeignKey(Player, default = 0)
    tournament = models.ForeignKey(Tournament, default = 0)
    
    def __str__(self):
        return "Code of " + str(self.player) + " for the " + str(self.tournament)  
    
    
class WebSiteInfo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null = True)
    
    def __str__(self):
        return "Information of the " + str(self.name) + " web site."
    

    
    
# Signals

def schedule_run_tournament(sender, instance, created, **kwargs):
    if created or instance.datetime != instance.last_datetime:  
        print("Hora de inicio cambiada.")
        call_run_tournament.apply_async(eta=instance.datetime, args=[instance.pk, instance.datetime])
        instance.last_datetime = instance.datetime
        instance.save()
    else:
        print("Hora de inicio no modificada.")
    
    # Verify the data of the tournament
    #if instance.minPlayers > instance.maxPlayers or datetime.now() > instance.datetime:
     #   instance.status = Tournament_Status.objects.get(name = "Unpublished")
    #  instance.save()
    
    
models.signals.post_save.connect(schedule_run_tournament, sender=Tournament)