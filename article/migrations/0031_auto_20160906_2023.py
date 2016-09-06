# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0030_collection_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='trash',
            field=models.BooleanField(default=False, verbose_name=b'Trash'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='collections',
            field=models.ManyToManyField(default=None, related_name='blogs', null=True, to='article.Collection'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='name',
            field=models.CharField(unique=True, max_length=100, verbose_name=b'Collection'),
        ),
    ]
