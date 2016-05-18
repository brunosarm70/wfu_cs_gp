# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0016_auto_20160510_0250'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='match_played',
            field=models.ForeignKey(to='gp.Match', default=0),
        ),
        migrations.AddField(
            model_name='competitor',
            name='tournament',
            field=models.ForeignKey(to='gp.Tournament', default=0),
        ),
    ]
