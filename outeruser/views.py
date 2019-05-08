from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from .models import *
from utils.common import *
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from xml.sax.saxutils import unescape
import logging

logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger(__name__)



'''判断用户登入状态'''
def login_check(func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('login_status'):
            return HttpResponseRedirect('/login/')
        return func(request, *args,** kwargs)

    return wrapper

'''登入接口'''
def login(request):

    if request.method == 'GET':
        return render(request,'login.html')
    if request.method == 'POST':
        usermsg = json.loads(request.body,encoding="utf-8")
        print(usermsg)
        username = usermsg['username']
        password = usermsg['password']
        if not username or not password:
            return fail_jsonresponse("账号或密码不能为空",100001)
        elif User.objects.filter(username__exact=username).count()==0:
            return fail_jsonresponse("账号不存在，请确认",100002)
        elif User.objects.filter(username__exact=username).filter(password__exact=password).count()==0:
            return fail_jsonresponse("密码错误，请确认",100003)
        elif User.objects.filter(username__exact=username).filter(password__exact=password).count()==1:
            request.session['login_status']=True
            request.session['new_account']=username
            return success_jsonresponse("登入成功!",100000)
        else:
            return fail_jsonresponse("操作失败",199999)

'''404跳转'''
def page_not_found(request):
    return render(request,"404.html")


'''注册'''
def register(request):

    if request.method == 'POST':
        dict = json.loads(request.body,encoding="utf-8")
        username = dict['username']
        password = dict['password']
        mail = dict['mail']
        if not username or not password or not mail:
            return fail_jsonresponse("账号、密码或邮箱不能为空",100001)
        elif User.objects.filter(username=username).count()>0:
            return fail_jsonresponse("该账号昵称已存在,请更换",100002)
        else:
            try:
                User.objects.create(username=username,password=password,mail=mail)
                return success_jsonresponse("恭喜你，账号注册成功！",100000)
            except Exception:
                return fail_jsonresponse("注册失败,数据库炸炸炸啦！！!",999999)

    if request.method == 'GET':
        return render(request,'register.html')

'''跳转到主页'''
@login_check
def index(request):
    username = request.session["new_account"]
    return render(request,"homepage.html",context=locals())

'''跳转到项目管理'''
@login_check
def project(request):
    username = request.session['new_account']
    context = {"username": username}
    return render(request,"project.html",context=locals())

'''登出'''
@login_check
def logout(request):

    #清除session信息
    del request.session['login_status']
    del request.session['new_account']
    return HttpResponseRedirect("/login")


'''新增项目'''
@login_check
def add_project(request):

    project_msg = json.loads(request.body,encoding="utf-8")
    projectname = project_msg["projectname"]
    testurl = project_msg["testurl"]
    yfburl = project_msg["yfburl"]
    devurl = project_msg["devurl"]
    xsurl = project_msg["xsurl"]
    devleader = project_msg["devleader"]
    testleader = project_msg["testleader"]

    if not projectname or not testurl or not yfburl or not devurl or not xsurl or not devleader or not testleader:
        return fail_jsonresponse("请检查是否有未填项！",100001)
    elif Project.objects.filter(projectname=projectname).count()>0:
        return fail_jsonresponse("该项目已存在，不允许重复添加！",100002)
    else:
        try:
            Project.objects.create(projectname=projectname,testurl=testurl,yfburl=yfburl,xsurl=xsurl,devurl=devurl,devleader=devleader,testleader=testleader)
            return success_jsonresponse("新增成功",100000)
        except Exception:
            return fail_jsonresponse("操作失败",999999)

'''查询'''
@login_check
def select_project(request):
    username = request.session['new_account']
    dic = request.GET
    projectname = dic.get("projectname")
    if not projectname or projectname=="":
        try:
            projects = Project.objects.all().order_by("-updatetime")
            '''分页功能，默认一页10条数据'''
            paginator = Paginator(projects,10)
            page = dic.get("page")
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(paginator.num_pages)
            projectname=""
            return render(request, "project.html",locals())
        except Exception as e:
            print(e)
            return fail_jsonresponse("查询失败",999999)
    else:
        try:
            projects = Project.objects.filter(projectname__icontains=projectname)
            paginator = Paginator(projects, 10)
            page = dic.get("page")
            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                contacts = paginator.page(1)
            except EmptyPage:
                contacts = paginator.page(paginator.num_pages)
            print(locals())
            return render(request,"project.html",context=locals())

        except Exception as e:
            print(e)
            return fail_jsonresponse("查询失败",999999)


'''获取项目信息'''
@login_check
def get_project_msg(request):
    if request.method=="GET":
        projectid = unescape(request.GET.get("projectid"))
        projectmsg = Project.objects.filter(projectid=projectid)
        data = queryset_to_dict(projectmsg)
        return success_jsonresponse("查询成功",100000,data=data)

'''编辑项目信息'''
@login_check
def updateProject(request):

    if request.method == "GET":
        username = request.session['new_account']
        projectname = request.GET.get("projectname")
        selecttext = request.GET.get("selectText")
        if projectname:
            projects = Project.objects.filter(projectname=projectname).order_by("-updatetime")
        else:
            projects = Project.objects.order_by("-updatetime")
        '''分页功能，默认一页10条数据'''
        paginator = Paginator(projects, 10)
        page = request.GET.get("page")
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        return render(request,"project.html",locals())
    else:
        dic = json.loads(request.body)
        projectid = dic["projectid"]
        projectname = dic["projectname"]
        testurl = dic["testurl"]
        yfburl = dic["yfburl"]
        devurl = dic["devurl"]
        xsurl = dic["xsurl"]
        devleader = dic["devleader"]
        testleader = dic["testleader"]
        if not projectname or not testurl or not yfburl or not devurl or not xsurl or not devleader or not testleader:
            return fail_jsonresponse("请检查是否有未填项！", 100001)
        try:
            project = Project.objects.filter(projectid=projectid).first()
            project.projectname = projectname
            project.testurl = testurl
            project.yfburl = yfburl
            project.devurl = devurl
            project.xsurl = xsurl
            project.devleader = devleader
            project.testleader = testleader
            project.save()
            return success_jsonresponse("更新成功",100000)
        except Exception as e:
            print(e)
            return fail_jsonresponse("操作失败",999999)

'''删除项目'''
@login_check
def deleteProject(request):

    dic = json.loads(request.body)
    projectname = dic["projectname"]
    try:
        Project.objects.filter(projectname=projectname).delete()
        return success_jsonresponse("删除成功",100000)
    except Exception:
        return fail_jsonresponse("删除失败",999999)

@login_check
def homepage(request):
    username = request.session.get("new_account")
    return render(request,"homepage.html",locals())


'''查询模块'''
@login_check
def module(request):
    username = request.session['new_account']
    projects = Project.objects.all()
    modules = []
    paginator = None
    if request.method == "GET":
        projectname = request.GET.get("projectname")
        modulename = request.GET.get("modulename")
        page = request.GET.get("page")
        if modulename and projectname!='':
            try:
                projectid = Project.objects.get(projectname=projectname).projectid
                modules = Module.objects.filter(modulename__icontains=modulename,project_id=projectid).order_by("-updatetime")
                paginator = Paginator(modules, 10)
            except Exception as e:
                print(e)
        elif projectname and projectname!='请选择':
            try:
                projectid = Project.objects.get(projectname=projectname).projectid
                modules = Module.objects.filter(project_id=projectid).order_by("-updatetime")
                paginator = Paginator(modules, 10)
                modulename = ""
            except Exception as e:
                print(e)
        else:
            modules = Module.objects.all().order_by("-updatetime")
            paginator = Paginator(modules, 10)

        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        return render(request, "module.html", locals())



'''新增模块'''
@login_check
def add_module(request):

    dic = json.loads(request.body)
    projectname = dic.get("projectname")
    projectid = Project.objects.get(projectname=projectname).projectid
    modulename = dic.get("modulename")
    devleader = dic.get("devleader")
    testleader = dic.get("testleader")
    project = Project.objects.get(projectname=projectname)
    if not projectname or not modulename or not devleader or not testleader:
        return fail_jsonresponse("请检查是否有字段为空！",100001)
    elif Module.objects.filter(project_id=projectid,modulename=modulename).count()>0:
        return fail_jsonresponse("该模块已存在！禁止重复添加",100002)
    else:
        try:
            module_dict={"project":project,"modulename":modulename,"devleader":devleader,"testleader":testleader}
            Module.objects.create(**module_dict)
            return success_jsonresponse("新增成功",100000)
        except Exception as e:
            print("异常信息====》"+e)
            return fail_jsonresponse("操作失败",999999)


'''
    根据模块名获取模块信息
'''
@login_check
def get_module_msg(request):

    modulename = request.GET.get("modulename")

    if modulename:
        module = Module.objects.filter(modulename=modulename)
        data = queryset_to_dict(module)
        return success_jsonresponse("查询成功", 100000, data=data)
    else:
        return fail_jsonresponse("模块名不能为空",100001)

'''编辑模块信息'''

def updateModule(request):

    dic = json.loads(request.body)
    moduleid = dic['moduleid']
    projectname = dic['projectname']
    modulename = dic['modulename']
    devleader = dic['devleader']
    testleader = dic['testleader']
    projectid = Project.objects.get(projectname=projectname).projectid
    if not projectname or not modulename or not devleader or not testleader:
        return fail_jsonresponse("请检查是否有未填项",100001)
    elif Module.objects.filter(project_id=projectid).count()==0:
        return fail_jsonresponse("未找到对应项目",100002)
    else:
        module = Module.objects.filter(moduleid=moduleid).first()
        module.modulename = modulename
        module.devleader = devleader
        module.testleader = testleader
        module.save()
        return success_jsonresponse("更新成功",100000)

'''删除模块信息'''
@login_check
def deleteModule(request):

    dic = json.loads(request.body)
    modulename = dic['modulename']
    if(modulename):
        try:
            Module.objects.filter(modulename=modulename).delete()
            return success_jsonresponse("删除成功",100000)
        except Exception:
            return fail_jsonresponse("删除失败，后台出错啦~",999999)
    else:
        return fail_jsonresponse("模块名称不允许为空",100001)


'''接口管理跳转'''
@login_check
def api(request):
    username = request.session.get("new_account")
    if request.method == 'GET':
        projects = Project.objects.all()
        return render(request,"api.html",locals())


'''根据项目查询模块'''
@login_check
def get_module_by_project(request):
    if request.method == 'GET':
        selproject=request.GET.get("projectname")
        if selproject:
            try:
                projectid=Project.objects.get(projectname=selproject).projectid
                modules = Module.objects.filter(project_id=projectid)
                data = queryset_to_dict(modules)
                return success_jsonresponse("查询成功",100000,data=data)
            except Exception:
                return fail_jsonresponse("操作失败",999999)
        else:
            return fail_jsonresponse("模块名称不能为空",100057)

'''新增接口'''
@login_check
def add_api(request):
    if request.method == 'POST':
        dic = json.loads(request.body)
        moduleid = dic["moduleid"]
        apiname = dic["apiname"]
        apimethod = dic["apimethod"]
        apiurl = dic["apiurl"]
        testleader = dic["testleader"]
        if Api.objects.filter(name=apiname).count()>0:
            return fail_jsonresponse("该接口名称已存在",100050)
        elif Api.objects.filter(url=apiurl).count()>0:
            return fail_jsonresponse("该接口地址已存在",100051)
        else:
            try:
                module = Module.objects.get(moduleid=moduleid)
                project = Module.objects.get(moduleid=moduleid).project
                api = {"module":module,"name":apiname,"method":apimethod,
                       "url":apiurl,"testleader":testleader,"project":project
                       }
                Api.objects.create(**api)
                return success_jsonresponse("操作成功",100000)
            except Exception as e:
                print(e)
                return fail_jsonresponse("操作失败",999999)

'''查询接口'''
@login_check
def select_api(request):
    username = request.session.get("new_account")
    if request.method == 'GET':
        projects = Project.objects.all()
        projectname =request.GET.get("projectname")
        moduleid = request.GET.get("moduleid")
        if moduleid:
            moduleid = int(moduleid)
        method = request.GET.get("apimethod")
        url = request.GET.get("apiurl")
        name = request.GET.get("apiname")
        page = request.GET.get("page")
        if projectname:
            project = Project.objects.get(projectname=projectname)
            modules = Module.objects.filter(project=project)
            if moduleid:

                module = Module.objects.get(moduleid=moduleid)
                if method:
                    apis = Api.objects.filter(project=project,module=module,method=method,url__icontains=url,name__icontains=name).order_by("-updatetime")
                else:
                    apis = Api.objects.filter(project=project, module=module, url__icontains=url,
                                              name__icontains=name).order_by("-updatetime")
            elif method:
                apis = Api.objects.filter(project=project,method=method,url__icontains=url,name__icontains=name).order_by("-updatetime")
            else:
                apis = Api.objects.filter(project=project,url__icontains=url,name__icontains=name).order_by("-updatetime")
        elif method:
            apis = Api.objects.filter(method=method,url__icontains=url,name__icontains=name).order_by("-updatetime")
        else:
            apis = Api.objects.all().order_by("-updatetime")
        #分页
        paginator = Paginator(apis, 10)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        return render(request,"api.html",locals())



'''根据接口名查询详情'''
@login_check
def get_api_msg(request):

    apiid = request.GET.get("apiid")

    if apiid:
        api = Api.objects.filter(apiid=apiid)
        data = queryset_to_dict(api)
        return success_jsonresponse("查询成功", 100000, data=data)
    else:
        return fail_jsonresponse("接口名不能为空",100001)

'''编辑接口'''
@login_check
def update_api(request):

    if request.method == 'POST':
        dic = json.loads(request.body)
        apiid = dic["apiid"]
        apiname = dic["apiname"]
        apimethod = dic["apimethod"]
        apiurl = dic["apiurl"]
        testleader = dic["testleader"]

        try:
            api = Api.objects.get(apiid=apiid)
            api.name = apiname
            api.method = apimethod
            api.url = apiurl
            api.testleader = testleader
            api.save()
            return success_jsonresponse("更新成功",100000)
        except Exception as e:
            print(e)
            return fail_jsonresponse("更新失败",999999)

'''删除接口'''
@login_check
def delete_api(request):

    if request.method == 'POST':
        dic = json.loads(request.body)
        apiid = dic["apiid"]
        if apiid:
            try:
                api = Api.objects.get(apiid=apiid)
                api.delete()
                return success_jsonresponse("删除成功",100000)
            except Exception:
                return fail_jsonresponse("操作失败",999999)
        else:
            return fail_jsonresponse("id不允许为空",100001)

@login_check
def case(request):
    '''
    用例管理页面跳转
    :param request:
    :return:
    '''
    username = request.session.get("new_account")
    if request.method == 'GET':
        apiid = request.GET.get("apiid")
        page = request.GET.get("page")
        apis = Api.objects.all().order_by("-updatetime")
        paginator = None
        if apiid:
            api = Api.objects.get(apiid=apiid)
            cases = Case.objects.filter(api=api).order_by("-updatetime")
        else:
            cases = Case.objects.all().order_by("-updatetime")
        paginator = Paginator(cases, 10)
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        return render(request,"case.html",locals())


def add_case(request):
    '''
    新增用例
    :param request:
    :return:
    '''
    if request.method == 'POST':
        try:
            dic = json.loads(request.body)
            url = dic.get("requestMsg").get("url")
            name = dic.get("requestMsg").get("name")
            method = dic.get("requestMsg").get("method")
            headers = dic.get("requestMsg").get("headers").encode("utf-8")
            body = dic.get("requestMsg").get("body").encode("utf-8")
            params = dic.get("requestMsg").get("params")
            assertion = dic.get("requestMsg").get("assertion")
            api_id = dic.get("apiId")
            person = dic.get("person")
            #case实体对象
            case = {"url":url,"name":name,"method":method,"headers":headers,"body":body,"params":params,"assertion":
                   assertion,"api_id":api_id,"person":person}
            Case.objects.create(**case)
            return success_jsonresponse("操作成功",100000)
        except:
            return fail_jsonresponse("操作失败",999999)














