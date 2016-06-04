# -*- coding: utf-8 -*-
#from django.conf.urls.defaults import patterns, url
from django.conf.urls import patterns, url

urlpatterns = patterns('myproject.wordlists.views',
    url(r'^list/$',     'list_wordlists',           name='list_wordlists'),
    url(r'^new/$',      'add_new_wordlist',         name='add_new_wordlist'),
    url(r'^edit/(.*)$', 'add_new_wordlist',         name='edit'),
    url(r'^show/(.*)$', 'show',                     name='show'),
    url(r'^add_words/(.*)$',  'add_words',          name='add_words'),
)
