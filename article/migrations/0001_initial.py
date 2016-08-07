# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'Title')),
                ('category', models.CharField(max_length=50, verbose_name=b'Category', blank=True)),
                ('date_time', models.DateField(auto_now_add=True, verbose_name=b'Creation Date')),
                ('content', models.TextField(null=True, verbose_name=b'Content', blank=True)),
            ],
            options={
                'ordering': ['-date_time'],
            },
        ),
    ]
