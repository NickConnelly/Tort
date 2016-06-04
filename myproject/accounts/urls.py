# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('myproject.accounts.views',
) + patterns('',
    #url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    #url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^profile/$', TemplateView.as_view(template_name="profile.html"), name='profile'),
    (r'', include('userena.urls')), 
)
