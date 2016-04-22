from django.db import models
from django.utils import timezone
from datetime import date



# Create your models here.

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
    
    def __str__(self):
        return self.name
    
    
class Tournament_Status(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
    
class Tournament_Type(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
    
class Score(models.Model):
    score = models.IntegerField(default = 0)
    game_number = models.IntegerField(default = 0)
    
    def __str__(self):
        return str(score) + " in game #" + str(self.game_number)

    
class Competitor(models.Model):
    player = models.ForeignKey(Player, default = 0)
    won_games = models.IntegerField(default = 0)
    scores = models.ManyToManyField(Score, blank = True)
    
    def __str__(self):
        return "Competitor " + self.player
    
    
    
class Match(models.Model):
    competitors = models.ManyToManyField(Competitor)
    winner = models.ForeignKey(Player, null = True)
    round_number = models.IntegerField(default = 0)
    datetime = models.DateTimeField(null = True, default = None)
    
    def __str__(self):
        return "Match"
    
    
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    minPlayers = models.IntegerField(default = 0)
    maxPlayers = models.IntegerField(default = 0)
    status = models.CharField(max_length=100)
    game = models.ForeignKey(Game, default = 0)
    tournament_type = models.CharField(max_length=100)
    matches = models.ManyToManyField(Match, blank = True)
    datetime = models.DateTimeField(null = True, default = None)
    description = models.TextField(null = True)
    
    def __str__(self):
        return self.name
    
    
class Code(models.Model):
    url = models.FileField()
    player = models.ForeignKey(Player, default = 0)
    tournament = models.ForeignKey(Tournament, default = 0)
    
    def __str__(self):
        return "Code of " + self.player + " for the " + self.tournament    