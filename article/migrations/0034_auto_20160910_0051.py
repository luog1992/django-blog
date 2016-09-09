# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0033_remove_blog_valid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['category', 'title']},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['color']},
        ),
        migrations.AddField(
            model_name='category',
            name='public',
            field=models.BooleanField(default=True, verbose_name=b'Public'),
        ),
    ]
