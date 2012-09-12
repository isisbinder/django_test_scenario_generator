# -*- coding: utf-8 -*-
"""
   urls
   ~~~~~~

   Arquivo com definição dos URLs para acesso à aplicação.


   Aplicações executadas
   ----------------------

   | *Gerador de roteiros*
   | Gera roteiros de teste baseado em mapas mentais criados no Freemind.


   :copyright: (c) 2012 by Ísis Binder at COPEL

"""

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    (r'^django_apps/gerador_roteiros', include('gerador_roteiros.urls')),

)
