# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='alias',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='group',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='group',
            name='name',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='group',
            name='tags',
            field=models.TextField(default=''),
        ),
    ]
