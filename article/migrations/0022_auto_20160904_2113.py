# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0021_auto_20160902_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(default=b'@sum<br>Summary your blog here...<br>@endsum<br><hr>', verbose_name=b'Content'),
        ),
    ]
