# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-05 02:30
from __future__ import unicode_literals

import core.models
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20160405_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='capsule',
            name='retired',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='capsule',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(core.models.make_rng_filename, *('files',), **{})),
        ),
    ]