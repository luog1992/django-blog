# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_auto_20160824_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='summary',
            field=models.CharField(max_length=1000, null=True, verbose_name=b'Summary', blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=20, verbose_name=b'Category'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=20, verbose_name=b'Tag'),
        ),
    ]
