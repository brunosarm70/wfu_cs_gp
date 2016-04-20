# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gp', '0004_auto_20160414_2327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='email',
        ),
        migrations.RemoveField(
            model_name='player',
            name='firstName',
        ),
        migrations.RemoveField(
            model_name='player',
            name='lastName',
        ),
        migrations.RemoveField(
            model_name='player',
            name='password',
        ),
        migrations.AddField(
            model_name='player',
            name='user',
            field=models.ForeignKey(default=0, to=settings.AUTH_USER_MODEL),
        ),
    ]
