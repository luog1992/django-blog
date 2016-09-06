# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0031_auto_20160906_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='collections',
            field=models.ManyToManyField(related_name='blogs', to='article.Collection'),
        ),
    ]
