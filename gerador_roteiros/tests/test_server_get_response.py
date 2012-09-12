# -*- coding: utf-8 -*-
import logging
from django.core.urlresolvers import reverse
from django.test.client import Client

django_client = Client()
test_logger = logging.getLogger(__name__)
test_logger.addHandler(logging.FileHandler('generator_validation_test_results.log','w'))


def test_get_response():
  """Verifica se o servidor responde à requisição GET com o código 405."""
  test_logger.info('Executando os testes...[{0}]'.format(__name__))
  response = django_client.get(reverse('gerador'))
  assert response.status_code == 405