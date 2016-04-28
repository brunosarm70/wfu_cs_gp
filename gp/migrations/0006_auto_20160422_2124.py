# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0005_auto_20160420_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='url',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
