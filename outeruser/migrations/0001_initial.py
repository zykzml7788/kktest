# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Api',
            fields=[
                ('apiid', models.AutoField(verbose_name='id', primary_key=True, serialize=False)),
                ('name', models.CharField(verbose_name='接口名称', max_length=15)),
                ('url', models.CharField(verbose_name='接口地址', max_length=50)),
                ('method', models.CharField(verbose_name='请求方式', max_length=10)),
                ('casenum', models.IntegerField(verbose_name='用例数', default=0)),
                ('testleader', models.CharField(verbose_name='测试负责人', max_length=10, default=None)),
                ('createtime', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('updatetime', models.DateTimeField(verbose_name='修改时间', auto_now=True)),
            ],
            options={
                'verbose_name': '接口表',
                'db_table': 't_api',
            },
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('caseid', models.AutoField(verbose_name='id', primary_key=True, serialize=False)),
                ('url', models.CharField(verbose_name='接口地址', max_length=100)),
                ('name', models.CharField(verbose_name='用例名称', max_length=30)),
                ('method', models.CharField(verbose_name='请求方式', max_length=10)),
                ('body', models.TextField(verbose_name='请求体', max_length=21845)),
                ('headers', models.CharField(verbose_name='请求头', max_length=1000)),
                ('params', models.TextField(verbose_name='请求参数', max_length=21845)),
                ('assertion', models.TextField(verbose_name='断言', max_length=10000)),
                ('person', models.CharField(verbose_name='编写人', max_length=10)),
                ('createtime', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('updatetime', models.DateTimeField(verbose_name='修改时间', auto_now=True)),
                ('api', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='outeruser.Api')),
            ],
            options={
                'verbose_name': '用例表',
                'db_table': 't_case',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('moduleid', models.AutoField(verbose_name='id', primary_key=True, serialize=False)),
                ('modulename', models.CharField(verbose_name='模块名称', max_length=10)),
                ('devleader', models.CharField(verbose_name='开发负责人', max_length=10)),
                ('testleader', models.CharField(verbose_name='测试负责人', max_length=10)),
                ('createtime', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('updatetime', models.DateTimeField(verbose_name='修改时间', auto_now=True)),
            ],
            options={
                'verbose_name': '模块表',
                'db_table': 't_module',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('projectid', models.AutoField(verbose_name='id', primary_key=True, serialize=False)),
                ('projectname', models.CharField(verbose_name='项目名称', max_length=30)),
                ('testurl', models.CharField(verbose_name='项目测试环境地址', max_length=30)),
                ('yfburl', models.CharField(verbose_name='项目预发布环境地址', max_length=30)),
                ('devurl', models.CharField(verbose_name='项目开发环境地址', max_length=30)),
                ('xsurl', models.CharField(verbose_name='项目线上环境地址', max_length=30)),
                ('devleader', models.CharField(verbose_name='项目开发负责人', max_length=10)),
                ('testleader', models.CharField(verbose_name='项目测试负责人', max_length=10)),
                ('createtime', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('updatetime', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
            ],
            options={
                'verbose_name': '项目表',
                'db_table': 't_project',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.AutoField(verbose_name='id', primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=20)),
                ('mail', models.CharField(max_length=20)),
                ('createtime', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('updatetime', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
            ],
            options={
                'verbose_name': '用户表',
                'db_table': 't_user',
            },
        ),
        migrations.AddField(
            model_name='module',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='outeruser.Project'),
        ),
        migrations.AddField(
            model_name='api',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='outeruser.Module'),
        ),
        migrations.AddField(
            model_name='api',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='outeruser.Project'),
        ),
    ]
