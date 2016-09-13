# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0036_auto_20160910_1442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='trash',
        ),
        migrations.AddField(
            model_name='blog',
            name='valid',
            field=models.BooleanField(default=True, verbose_name=b'Valid'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(default=b'@sum<br>Summary your blog here...<br>@endsum', verbose_name=b'Content'),
        ),
    ]
