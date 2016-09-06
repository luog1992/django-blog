# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0032_auto_20160906_2246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='valid',
        ),
    ]
