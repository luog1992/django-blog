# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_aa_bb_cc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name=b'category')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name=b'tag')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.RemoveField(
            model_name='bb',
            name='aa',
        ),
        migrations.RemoveField(
            model_name='cc',
            name='bb',
        ),
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.DeleteModel(
            name='AA',
        ),
        migrations.DeleteModel(
            name='BB',
        ),
        migrations.DeleteModel(
            name='CC',
        ),
        migrations.AddField(
            model_name='category',
            name='articles',
            field=models.ManyToManyField(to='article.Article'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='article.Tag'),
        ),
    ]
