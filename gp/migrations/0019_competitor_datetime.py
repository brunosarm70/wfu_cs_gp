# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0018_auto_20160511_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitor',
            name='datetime',
            field=models.DateTimeField(null=True, default=None),
        ),
    ]
