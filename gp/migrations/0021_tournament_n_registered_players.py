# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0020_websiteinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='n_registered_players',
            field=models.IntegerField(default=0),
        ),
    ]
