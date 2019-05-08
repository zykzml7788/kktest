import json
from django.http import *
from django.core import serializers

'''返回一个标准的成功响应jsonResponse'''
def success_jsonresponse(msg,code,data=None):
    responsedict = {"msg":msg,"code":code,"data":data,"success":True}
    jsonstr = json.dumps(responsedict,ensure_ascii=False)
    return HttpResponse(jsonstr,content_type="application/json;charset=utf-8")

'''返回一个标准的失败响应jsonResponse'''
def fail_jsonresponse(msg,code,data=None):
    responsedict = {"msg":msg,"code":code,"data":data,"success":False}
    jsonstr = json.dumps(responsedict,ensure_ascii=False)
    return HttpResponse(jsonstr,content_type="application/json;charset=utf-8")


# objects.get()结果转换
def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])

# queryset转换为dict
def queryset_to_dict(queryset):
    js=serializers.serialize("json", queryset, ensure_ascii=False)
    return json.loads(js)