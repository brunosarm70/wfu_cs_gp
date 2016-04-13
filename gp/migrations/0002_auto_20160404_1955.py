# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='matches',
            field=models.ManyToManyField(to='gp.Match', blank=True),
        ),
    ]
