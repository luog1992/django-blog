# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20160814_1220'),
    ]

    operations = [
        migrations.CreateModel(
            name='AA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aaname', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BB',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bbname', models.CharField(max_length=100)),
                ('aa', models.ManyToManyField(to='article.AA')),
            ],
        ),
        migrations.CreateModel(
            name='CC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ccname', models.CharField(max_length=100)),
                ('bb', models.ManyToManyField(to='article.BB')),
            ],
        ),
    ]
