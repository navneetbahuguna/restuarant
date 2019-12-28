"""pro1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
#from view import index
#from polls import about
#from django.urls import path
#from django.urls import path


'''from polls.about import about
from polls.home import index
from polls.branch import branch
from polls.contact import contact
from polls.form import form
from templates import print11'''
from polls.views import about,branch,contact,form,index,home,capImage
#from polls.image_cap import requested_url
#from polls.views import index

urlpatterns = [
    
    url('about', about,name='about'),
    url('home', home,name='home'),
    url('contact', contact,name='contact'),
    url('branch', branch,name='branch'),
    url('form', form,name='form'),
    url('capImage',capImage,name='capImage'),
    url('',index,name='index'),
    

]
