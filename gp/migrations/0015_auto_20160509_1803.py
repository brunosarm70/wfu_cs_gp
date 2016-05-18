# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0014_auto_20160509_0600'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='function_player_name',
            field=models.CharField(max_length=100, default='function_name'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='winner',
            field=models.ForeignKey(null=True, to='gp.Player', blank=True),
        ),
    ]
