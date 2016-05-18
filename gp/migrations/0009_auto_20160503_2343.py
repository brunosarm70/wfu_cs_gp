# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0008_auto_20160425_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='status',
            field=models.ForeignKey(to='gp.Tournament_Status', default=0),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='tournament_type',
            field=models.ForeignKey(to='gp.Tournament_Type', default=0),
        ),
    ]
