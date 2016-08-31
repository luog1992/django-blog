# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0014_auto_20160831_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='status',
            field=models.CharField(default=b'DRAFT', max_length=7, verbose_name=b'Status', choices=[(b'DRAFT', b'Draft'), (b'PUBLIC', b'Public'), (b'PRIVATE', b'Private')]),
        ),
    ]
