# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0019_auto_20160901_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(default=b'@sum<br><br>Summary your blog here...<br><br>@endsum<br><br><hr>', verbose_name=b'Content'),
        ),
    ]
