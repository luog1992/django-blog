# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_auto_20160825_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='summary',
            field=models.TextField(max_length=1000, null=True, verbose_name=b'Summary', blank=True),
        ),
    ]
