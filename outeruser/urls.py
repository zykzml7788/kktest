from django.conf.urls import include, url
from outeruser import views


urlpatterns = [
    url(r'login', views.login),
    url(r'register', views.register),
    url(r'index',views.index),
    url(r'logout',views.logout),
    url(r'project',views.project),
    url(r'addProject',views.add_project),
    url(r'selectProject',views.select_project),
    url(r'getProjectMsg',views.get_project_msg),
    url(r'editProject',views.updateProject),
    url(r'deleteProject',views.deleteProject),
    url(r'homepage',views.homepage),
    url(r'module',views.module),
    url(r'addModule',views.add_module),
    url(r'getModuleMsg',views.get_module_msg),
    url(r'deleteModule',views.deleteModule),
    url(r'editModule',views.updateModule),
    url(r'api',views.api),
    url(r'getModulesByProjectname',views.get_module_by_project),
    url(r'addApi',views.add_api),
    url(r'selectApi',views.select_api),
    url(r'getApiMsg',views.get_api_msg),
    url(r'updateApi',views.update_api),
    url(r'deleteApi',views.delete_api),
    url(r'case',views.case),
    url(r'addCase',views.add_case),
]

handler404 = views.page_not_found
