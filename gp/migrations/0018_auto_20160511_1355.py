# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0017_auto_20160510_0305'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tournament',
            old_name='number_of_games_per_match',
            new_name='games_to_win_the_match',
        ),
    ]
