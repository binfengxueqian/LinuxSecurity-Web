"""LinuxSecurity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from webadmin import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login',views.login.as_view()),
    url(r'index',views.index),
    url(r'home',views.home),
    url(r'developer',views.developer.as_view()),
    url(r'setTimer',views.Timer.as_view()),
    url(r'task_msg',views.task_msg.as_view()),
    url(r'initdbshow',views.initdbshow.as_view()),
    url(r'checkdbshow',views.checkdbshow.as_view()),
    url(r'log.html', views.log),
    url(r'BindSubdevice.html',views.bindSubDevice.as_view()),
    url(r'checkPassword',views.checkPassword),
    url(r'admin_changepass',views.admin_changepass.as_view()),
    url(r'favicon.ico',RedirectView.as_view(url=r'static/images/favicon.ico')),
    url(r'^$',views.index)
]