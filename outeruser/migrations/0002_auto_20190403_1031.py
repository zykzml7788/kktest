# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outeruser', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='assertion',
            field=models.TextField(verbose_name='断言'),
        ),
        migrations.AlterField(
            model_name='case',
            name='body',
            field=models.TextField(verbose_name='请求体'),
        ),
        migrations.AlterField(
            model_name='case',
            name='params',
            field=models.TextField(verbose_name='请求参数'),
        ),
    ]
