# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20160825_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(default=b'transparent', max_length=20, verbose_name=b'Color'),
        ),
        migrations.AddField(
            model_name='tag',
            name='color',
            field=models.CharField(default=b'transparent', max_length=20, verbose_name=b'Color'),
        ),
    ]
