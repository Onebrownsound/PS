# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-21 19:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Capsule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('message', models.TextField(blank=True, default='', max_length=10000)),
                ('file', models.FileField(blank=True, upload_to='')),
                ('activation', models.CharField(choices=[('D', 'Death Activation'), ('T', 'Time Activation')], default='D', max_length=10)),
                ('time_activation', models.DateTimeField(blank=True)),
                ('delivery', models.CharField(choices=[('SD', 'Specific Date In Future'), ('W', 'Wedding'), ('CB', 'Child Birth')], default='SD', max_length=10)),
                ('time_delivery', models.DateTimeField(blank=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capsules', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]