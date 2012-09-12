# -*- coding: utf-8 -*-
"""
   validators.relaxngValidator
   ~~~~~~~~

   Contém a classe que realizará a validação utilizando o esquema RelaxNG.

   :copyright: (c) 2012 by Ísis Binder at COPEL

"""
import os
import lxml
from lxml import etree
from django.template.loader import get_template
from django.template import Context
from gerador_roteiros.datatypes.exceptions import RelaxNGValidationException, UnsupportedVersionException


class FreemindRelaxNGValidator(object):
  """Classe para validação do mapa mental utilizando esquemas RelaxNG."""

  SCHEMA_PATH = os.sep.join([os.path.split(os.path.dirname(__file__))[0], 'schemas'])
  SCHEMA_FILENAME_PATTERN = 'freemind_{0}.rng'


  def _read_rng_file(self):
    """Importa o esquema de validação correspondente à versão do Freemind
       informada na inicialização do objeto.
    """
    validator_filename = FreemindRelaxNGValidator.SCHEMA_FILENAME_PATTERN.format(self._freemind_version.replace('.',''))
    rng_file = etree.parse(os.sep.join([self._schema_path, validator_filename]))
    self._rng_schema = etree.RelaxNG(rng_file)



  def __init__(self, version, schema_path = SCHEMA_PATH):
    """Método responsável pela inicialização do validador RelaxNG.

       Argumentos
       -----------

       version é uma string contendo a versão do Freemind utilizada na
       elaboração do mapa mental.

       schema_path define o caminho absoluto do diretório onde se localizam os
       esquemas RelaxNG. Seu valor padrão é FreemindRelaxNGValidator.SCHEMA_PATH.

       Exceções
       ---------

       UnsupportedVersionException - lançada se não houver um esquema relaxng
       para a versão do Freemind usada na elaboração do mapa mental.

    """
    self._freemind_version = version
    self._schema_path = schema_path

    try:
      self._read_rng_file()

    except IOError:
      raise UnsupportedVersionException("A versão do Freemind utilizada na elaboração do mapa mental não possui um esquema RelaxNG próprio para validação.")



  def validate_mindmap(self, mindmap_content):
    """Realiza a validação do mapa mental.

       Argumentos
       -----------

       mindmap_content é o conteúdo do mapa mental em formato string,
       que será convertida para um documento XML e validada com o esquema
       RelaxNG importado durante a inicialização do objeto.

    """
    mindmap_file = etree.fromstring(mindmap_content)
    self._validation_status = self._rng_schema.validate(mindmap_file)
    if not self._validation_status:
      raise RelaxNGValidationException('O mapa mental não foi elaborado corretamente.\n')



  def _log_to_string(self):
    """Converte as mensagens do log de erros da validação RNG para string."""
    error_message = ''
    for error_entry in self._rng_schema.error_log:
      error_message = error_message + str(error_entry.level_name) + ': ' + str(error_entry.message) + '\n'
    return error_message



  def build_bad_xml(self, complementary_msg = ''):
    """Gera o XML para relatar erro na validação com RelaxNG.

       Argumentos
       -----------

       complementary_msg contém um texto complementar ao log da validação.
       Ambos serão inseridos no XML.

    """
    errors = complementary_msg + self._log_to_string()
    template = get_template('gerador_roteiros/generic_template.xml')
    context = Context({'validation_status': False, 'error_message': errors})
    return template.render(context)