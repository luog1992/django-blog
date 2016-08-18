# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='A',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aname', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='B',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bname', models.CharField(max_length=100)),
                ('aa', models.ManyToManyField(to='article.A')),
            ],
        ),
        migrations.CreateModel(
            name='C',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cname', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='b',
            name='cc',
            field=models.ManyToManyField(to='article.C'),
        ),
    ]
