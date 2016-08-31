# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0016_auto_20160831_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='status',
        ),
        migrations.AddField(
            model_name='blog',
            name='public',
            field=models.BooleanField(default=False, verbose_name=b'Public'),
        ),
        migrations.AddField(
            model_name='blog',
            name='valid',
            field=models.BooleanField(default=False, verbose_name=b'Valid'),
        ),
    ]
