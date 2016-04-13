# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('url', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('minPlayers', models.IntegerField()),
                ('maxPlayers', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('round_number', models.IntegerField(default=0)),
                ('datetime', models.DateTimeField(default=None, null=True)),
                ('competitors', models.ManyToManyField(to='gp.Competitor')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('country', models.ForeignKey(default=0, to='gp.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('minPlayers', models.IntegerField(default=0)),
                ('maxPlayers', models.IntegerField(default=0)),
                ('status', models.CharField(max_length=100)),
                ('tournament_type', models.CharField(max_length=100)),
                ('datetime', models.DateTimeField(default=None, null=True)),
                ('game', models.ForeignKey(default=0, to='gp.Game')),
                ('matches', models.ManyToManyField(to='gp.Match')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament_Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=4)),
                ('country', models.ForeignKey(default=0, to='gp.Country')),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='university',
            field=models.ForeignKey(default=0, to='gp.University'),
        ),
        migrations.AddField(
            model_name='match',
            name='winner',
            field=models.ForeignKey(to='gp.Player', null=True),
        ),
        migrations.AddField(
            model_name='competitor',
            name='player',
            field=models.ForeignKey(default=0, to='gp.Player'),
        ),
        migrations.AddField(
            model_name='code',
            name='player',
            field=models.ForeignKey(default=0, to='gp.Player'),
        ),
        migrations.AddField(
            model_name='code',
            name='tournament',
            field=models.ForeignKey(default=0, to='gp.Tournament'),
        ),
    ]
