# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0013_auto_20160509_0557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='scores',
        ),
        migrations.AddField(
            model_name='tournament',
            name='winner',
            field=models.ForeignKey(to='gp.Player', null=True),
        ),
    ]
