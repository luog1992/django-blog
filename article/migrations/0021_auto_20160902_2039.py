# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0020_auto_20160901_0132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='public',
            field=models.BooleanField(default=True, verbose_name=b'Public'),
        ),
    ]
