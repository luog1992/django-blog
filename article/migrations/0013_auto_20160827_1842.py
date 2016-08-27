# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0012_auto_20160827_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name=b'Title')),
                ('date_time', models.DateField(auto_now_add=True, verbose_name=b'Creation Date')),
                ('summary', models.TextField(max_length=1000, null=True, verbose_name=b'Summary', blank=True)),
                ('content', models.TextField(default=b'', verbose_name=b'Content')),
                ('category', models.ForeignKey(related_name='blogs', default=None, to='article.Category', null=True)),
                ('tags', models.ManyToManyField(related_name='blogs', to='article.Tag')),
            ],
            options={
                'ordering': ['-date_time'],
            },
        ),
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.RemoveField(
            model_name='article',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]
