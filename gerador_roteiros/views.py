# -*- coding: utf-8 -*-
import re
from django.http import HttpResponse
from django.views.generic import View
from gerador_roteiros.datatypes.exceptions import *
from gerador_roteiros.datatypes.freemind.basefreemind import BaseFreemind
from gerador_roteiros.validators.relaxngValidator import FreemindRelaxNGValidator
from gerador_roteiros.datatypes.testsuite import TestSuiteGenerator



class ViewGeradorRoteiro(View):

  """View principal para processamento do mapa mental.

     Os dois métodos implementados são GET e POST, com respostas diferentes.

     | *GET*
     | Retorna o código 405, correspondente à mensagem "Not implemented".
     | Isso é utilizado para verificar se o servidor está respondendo.
     |
     | *POST*
     | Recebe o conteúdo do arquivo como parâmetro e realiza a conversão do
     | mapa mental para roteiros, retornando um XML para pós-processamento.

  """

  def get(self, request):
    """Implementação do método get simulando um método ausente em um webservice.
       Serve apenas para verificar se o servidor Django está respondendo.

    """
    return HttpResponse(status = 405)



  def _post_data_validator(self, request):
    """Responsável pela realização da validação completa do mapa mental antes
       do início do processamento para geração do grafo.

       Argumentos
       -----------

       request é o objeto HTTPRequest contendo os dados da requisição enviada
       pela rede ao servidor.

    """
    rng_validator, testsuite, return_value = None, None, None

    try:
      # Primeira etapa da validação - RelaxNG
      # Validação apenas da sintaxe do mapa mental.
      # Exceções lançadas: RelaxNGValidationException, UnsupportedVersionException
      version = BaseFreemind(request.body).extract_map_version()
      rng_validator = FreemindRelaxNGValidator(version)
      rng_validator.validate_mindmap(request.body)

      # Segunda etapa da validação - Suporte da versão do Freemind
      # Exceções lançadas: UnsupportedVersionException
      testsuite = TestSuiteGenerator(request.body)

      testsuite.validate()

    except RelaxNGValidationException, exception:
      return_value = rng_validator.build_bad_xml(complementary_msg = exception.message)

    except (UnsupportedVersionException, NodeTypeException, EmptyNodeException, UndefinedReferenceException, InvalidSequenceException), exception:
      return_value = TestSuiteGenerator.build_bad_xml(exception.message)

    return return_value, testsuite


  def _graph_builder(self, testsuite_obj):
    """Realiza a construção do grafo e executa validações necessárias.

       Argumentos
       -----------

       testsuite_obj é o objeto gerador dos roteiros, responsável em parte pela
       construção dos grafos.

    """
    testsuite_obj.build_graphs()


  def post(self, request):
    """Realiza a conversão do mapa mental para um XML contendo todos os roteiros."""

    validation_error_message, testsuite = self._post_data_validator(request)
    if validation_error_message: # XML para documento mal-formado.
      return HttpResponse(validation_error_message, 'text/xml')

    # Nenhuma mensagem de erro de validação foi gerada na primeira parte. Construir grafo.
    self._graph_builder(testsuite)
    return HttpResponse(testsuite.build_good_xml(), 'text/xml')