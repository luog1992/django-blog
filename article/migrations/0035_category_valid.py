# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0034_auto_20160910_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='valid',
            field=models.BooleanField(default=False, verbose_name=b'Valid'),
        ),
    ]
