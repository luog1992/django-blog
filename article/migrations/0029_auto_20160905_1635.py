# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0028_auto_20160905_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='color',
            field=models.CharField(default=b'#99CC99', max_length=20, verbose_name=b'Color'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(default=b'#99CC99', max_length=20, verbose_name=b'Color'),
        ),
    ]
