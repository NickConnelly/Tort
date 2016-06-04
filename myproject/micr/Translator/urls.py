# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('myproject.micr.Translator.translator',
    url(r'^maketranslate/$', 'maketranslate'),
)

urlpatterns += patterns('myproject.micr.Translator.Frequency_list',
    url(r'^Frequency_list/(.*)', 'Frequency_list'),
)

urlpatterns += patterns('myproject.micr.Translator.views',
    url(r'^list_frequency_lists/$', 'list_frequency_list'),
)

urlpatterns += patterns('myproject.micr.Translator.Frequency_list_functions',
    url(r'^demo_text/(.*)', 'converted', name='converted'),
)
