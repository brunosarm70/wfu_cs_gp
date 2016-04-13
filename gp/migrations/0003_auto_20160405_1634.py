# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0002_auto_20160404_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('game_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='competitor',
            old_name='score',
            new_name='won_games',
        ),
        migrations.AddField(
            model_name='competitor',
            name='scores',
            field=models.ManyToManyField(blank=True, to='gp.Score'),
        ),
    ]
