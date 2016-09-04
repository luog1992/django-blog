# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0025_auto_20160904_2338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name=b'Collection')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(default=b'#FFFFFF', max_length=20, verbose_name=b'Color'),
        ),
        migrations.AddField(
            model_name='blog',
            name='collections',
            field=models.ManyToManyField(default=None, related_name='blogs', to='article.Collection'),
        ),
    ]
