# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0027_auto_20160905_0040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(unique=True, max_length=20, verbose_name=b'Category'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='name',
            field=models.CharField(unique=True, max_length=20, verbose_name=b'Collection'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(unique=True, max_length=20, verbose_name=b'Tag'),
        ),
    ]
