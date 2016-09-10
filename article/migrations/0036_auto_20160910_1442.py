# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0035_category_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='valid',
            field=models.BooleanField(default=True, verbose_name=b'Valid'),
        ),
    ]
