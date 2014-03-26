'''
Created on Mar 17, 2014

@author: ronaldjosephdesmarais
'''
from django.conf.urls import patterns, url

from usermanagement import views

urlpatterns = patterns('', 
                       url(r'^$', views.index, name='index'),
                       url(r'^request/', views.data, name='data')
)