# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0010_tournament_last_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='controller',
            field=models.FileField(null=True, blank=True, upload_to='./controllers/'),
        ),
    ]
