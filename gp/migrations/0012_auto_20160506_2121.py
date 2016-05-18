# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0011_game_controller'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='numbers_of_games_per_match',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='tournament',
            name='players_per_match',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='maxPlayers',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='minPlayers',
            field=models.IntegerField(default=2),
        ),
    ]
