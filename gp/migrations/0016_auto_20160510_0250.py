# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0015_auto_20160509_1803'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='numbers_of_games_per_match',
            new_name='number_of_games_per_match',
        ),
    ]
