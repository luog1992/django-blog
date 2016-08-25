# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_auto_20160825_0304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='articles',
        ),
        migrations.RemoveField(
            model_name='category',
            name='color',
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(default=None, to='article.Category'),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(default=b'', verbose_name=b'Content'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(default=b'#BFE37C', max_length=20, verbose_name=b'Color'),
        ),
    ]
