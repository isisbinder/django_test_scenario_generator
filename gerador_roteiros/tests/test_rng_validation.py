# -*- coding: utf-8 -*-
import os
import logging
import glob
import lxml
from lxml import etree
from django.core.urlresolvers import reverse
from django.test.client import Client

MINDMAP_TESTFILES_BASEDIR = os.sep.join([os.path.dirname(os.path.abspath(__file__)), 'testfiles'])
RNGVALIDATION_TESTFILES_DIR = 'rngvalidation'

django_client = Client()
test_logger = logging.getLogger(__name__)
test_logger.addHandler(logging.FileHandler('relaxng_validation_test_results.log','w'))


def test_generator_function():
  test_logger.info('Executando os testes...')
  directories = os.listdir(MINDMAP_TESTFILES_BASEDIR)

  for testing_version in directories:
    test_abspath = os.sep.join([MINDMAP_TESTFILES_BASEDIR, testing_version, RNGVALIDATION_TESTFILES_DIR])
    for map_status in ['invalid', 'valid']:
      filenames = glob.glob(os.sep.join([test_abspath, map_status, '*.mm']))
      analysis_return_value = False if map_status == 'invalid' else True

      for f in filenames:
        yield run_validation, f, analysis_return_value



def run_validation(filename, analysis_return_value):
  test_logger.info("-" * 50)
  test_logger.info("Enviando arquivo \n " + filename)

  file_content = ''
  with open(filename, 'rb') as fp:
    file_content = fp.read()

  response = django_client.post(reverse('gerador'), data = file_content, content_type = 'text/xml')
  response_doc = etree.fromstring(response.content)
  test_logger.debug("\nConteúdo do XML de retorno:\n " + response.content)

  assert str(analysis_return_value) == response_doc.xpath('/testplan/@status')[0]