# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0017_auto_20160831_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(default=b'@sum\nsummary your blog here...\n@endsum', verbose_name=b'Content'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='summary',
            field=models.TextField(max_length=1000, null=True, verbose_name=b'Summary', blank=True),
        ),
    ]
