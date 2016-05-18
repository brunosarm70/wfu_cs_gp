# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0009_auto_20160503_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='last_datetime',
            field=models.DateTimeField(null=True, default=None),
        ),
    ]
