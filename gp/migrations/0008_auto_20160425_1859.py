# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0007_auto_20160422_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='url',
            field=models.FileField(null=True, upload_to='./codes/', blank=True),
        ),
    ]
