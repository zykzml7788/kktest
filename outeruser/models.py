from django.db import models

# Create your models here.

from django.db import models




class User(models.Model):
    class Meta:
        verbose_name = '用户表'
        db_table = 't_user'

    userid = models.AutoField("id",primary_key=True)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    mail =models.CharField(max_length=20)
    createtime = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    updatetime = models.DateTimeField(verbose_name='更新时间',auto_now=True)

class Project(models.Model):

    class Meta:
        verbose_name = '项目表'
        db_table = 't_project'

    projectid = models.AutoField("id",primary_key=True)
    projectname = models.CharField("项目名称",max_length=30)
    testurl = models.CharField("项目测试环境地址",max_length=30)
    yfburl = models.CharField("项目预发布环境地址",max_length=30)
    devurl = models.CharField("项目开发环境地址",max_length=30)
    xsurl = models.CharField("项目线上环境地址",max_length=30)
    devleader = models.CharField("项目开发负责人",max_length=10)
    testleader = models.CharField("项目测试负责人",max_length=10)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    updatetime = models.DateTimeField('更新时间', auto_now=True)


class Module(models.Model):

    class Meta:
        verbose_name = '模块表'
        db_table = 't_module'

    moduleid = models.AutoField("id",primary_key=True)
    project = models.ForeignKey("Project",on_delete=models.PROTECT)
    modulename = models.CharField("模块名称",max_length=10)
    devleader = models.CharField("开发负责人",max_length=10)
    testleader = models.CharField("测试负责人",max_length=10)
    createtime = models.DateTimeField("创建时间",auto_now_add=True)
    updatetime = models.DateTimeField("修改时间",auto_now=True)


class Api(models.Model):

    class Meta:
        verbose_name = '接口表'
        db_table = 't_api'

    apiid = models.AutoField("id",primary_key=True)
    module = models.ForeignKey("Module",on_delete=models.PROTECT)
    project = models.ForeignKey("Project",on_delete=models.PROTECT,default=None)
    name = models.CharField("接口名称",max_length=15)
    url = models.CharField("接口地址",max_length=50)
    method = models.CharField("请求方式",max_length=10)
    casenum = models.IntegerField("用例数",default=0)
    testleader = models.CharField("测试负责人",max_length=10,default=None)
    createtime = models.DateTimeField("创建时间", auto_now_add=True)
    updatetime = models.DateTimeField("修改时间", auto_now=True)


class Case(models.Model):

    class Meta:
        verbose_name = '用例表'
        db_table = 't_case'

    caseid = models.AutoField("id",primary_key=True)
    url = models.CharField("接口地址",max_length=100)
    name = models.CharField("用例名称",max_length=30)
    method = models.CharField("请求方式",max_length=10)
    body = models.TextField("请求体")
    headers = models.CharField("请求头",max_length=1000)
    params = models.TextField("请求参数")
    assertion = models.TextField("断言")
    api = models.ForeignKey("Api",on_delete=models.PROTECT)
    person = models.CharField("编写人",max_length=10)
    createtime = models.DateTimeField("创建时间", auto_now_add=True)
    updatetime = models.DateTimeField("修改时间", auto_now=True)
