# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0018_auto_20160831_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(default=b'\n        @sum\n        summary your blog here...\n        @endsum\n    ', verbose_name=b'Content'),
        ),
    ]
