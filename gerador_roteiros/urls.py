from django.conf.urls.defaults import *
from gerador_roteiros.views import ViewGeradorRoteiro

urlpatterns = patterns('gerador_roteiros',
    url(r'^/$', ViewGeradorRoteiro.as_view(), name = 'gerador'),
)
