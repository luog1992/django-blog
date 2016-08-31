# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0015_blog_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='summary',
            field=models.TextField(default=b'@sum\\nsummary your blog here...\\n@endsum', max_length=1000, null=True, verbose_name=b'Summary', blank=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(default=b'Untitle', max_length=100, verbose_name=b'Title'),
        ),
    ]
