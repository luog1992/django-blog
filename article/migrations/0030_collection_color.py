# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0029_auto_20160905_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='color',
            field=models.CharField(default=b'#99CC99', max_length=20, verbose_name=b'Color'),
        ),
    ]
