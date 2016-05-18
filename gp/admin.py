from django.contrib import admin
from .models import Country, University, Player, Tournament, Tournament_Status, Game, Code, Competitor, Match, Tournament_Type, Score, WebSiteInfo

admin.site.register(University)
admin.site.register(Country)
admin.site.register(Player)
admin.site.register(Tournament)
admin.site.register(Tournament_Status)
admin.site.register(Tournament_Type)
admin.site.register(Code)
admin.site.register(Game)
admin.site.register(Competitor)
admin.site.register(Match)
admin.site.register(Score)
admin.site.register(WebSiteInfo)