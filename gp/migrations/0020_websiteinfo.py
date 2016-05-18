# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gp', '0019_competitor_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebSiteInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(null=True)),
            ],
        ),
    ]
