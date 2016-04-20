# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0003_auto_20160405_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='rules',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='tournament',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
