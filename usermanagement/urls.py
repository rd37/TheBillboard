'''
Created on Mar 17, 2014

@author: ronaldjosephdesmarais
'''
from django.conf.urls import patterns, url

from usermanagement import views

urlpatterns = patterns('', 
                       url(r'^$', views.index, name='index'),
                       url(r'^request/', views.data, name='request'),
                       url(r'^system_login/', views.system_login, name='system_login'),
                       url(r'^system_register/', views.system_register, name='system_register')
)