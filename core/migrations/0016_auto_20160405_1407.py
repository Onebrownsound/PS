# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-05 14:07
from __future__ import unicode_literals

import core.models
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20160405_0245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capsule',
            name='delivery_condition',
            field=models.CharField(choices=[('SD', 'Specific Date In Future'), ('CB', 'Child Birth'), ('M', 'Marriage'), ('D', 'Death')], default='SD', max_length=10),
        ),
        migrations.AlterField(
            model_name='capsule',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=functools.partial(core.models.make_rng_filename, *('files',), **{})),
        ),
    ]
