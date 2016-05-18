# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0012_auto_20160506_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='scores',
            field=models.ManyToManyField(to='gp.Score', blank=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='competitors',
            field=models.ManyToManyField(to='gp.Competitor', blank=True),
        ),
    ]
