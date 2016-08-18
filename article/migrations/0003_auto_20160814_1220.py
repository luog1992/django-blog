# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20160814_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='b',
            name='aa',
        ),
        migrations.RemoveField(
            model_name='b',
            name='cc',
        ),
        migrations.DeleteModel(
            name='A',
        ),
        migrations.DeleteModel(
            name='B',
        ),
        migrations.DeleteModel(
            name='C',
        ),
    ]
