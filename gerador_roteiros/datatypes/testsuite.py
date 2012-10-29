# -*- coding: utf-8 -*-
"""
   gerador_roteiros.datatypes.testsuite
   ~~~~~~~~~~

   Define os tipos de dados como um wrapper para a geração de roteiros.

   Created: 22/08/2012

"""
import inspect
import networkx
from django.template.loader import get_template
from django.template import Context
from gerador_roteiros.datatypes.freemind.basefreemind import BaseFreemind
from gerador_roteiros.datatypes.freemind import freemindconcrete
from gerador_roteiros.datatypes.freemind.freemindconcrete import *
from gerador_roteiros.datatypes.graph.graphs import ScenarioGraph
from gerador_roteiros.datatypes.freemind.nodetypes import *
from gerador_roteiros.datatypes.exceptions import *


class TestSuiteGenerator(object):
  """
    gerador_roteiros.datatypes.testsuite.TestSuiteGenerator
    ~~~~~~~~~~

    Contém operações genéricas para geração dos grafos e roteiros de teste.

  """

  @staticmethod
  def build_bad_xml(error_message):
    """Gera o XML com as mensagens de erro das validações extras.

       Argumentos
       -----------

       error_message é uma string que será inserida no template do XML de erro.

    """
    template = get_template('gerador_roteiros/generic_template.xml')
    context = Context({'validation_status': False, 'error_message': error_message})
    return template.render(context)


  def _search_concrete_class(self):
    """Pesquisa pela classe freemind correta de acordo com a versão
       informada no mapa mental.

       Exceções
       ---------

       UnsupportedVersionException - lançada caso nenhuma classe dê suporte à
       versão do Freemind utilizada para criar o mapa mental.

    """
    classes_list = [cls[1] for cls in inspect.getmembers(freemindconcrete, inspect.isclass) if cls[1].__module__.split('.')[-1] == 'freemindconcrete']
    for cls in classes_list:
      if self._map_version in cls._versions:
        return cls
    raise UnsupportedVersionException('A versão utilizada para criar o mapa mental não é suportada pelo gerador.')


  def __init__(self, xml_content):
    """Inicializador que instancia um objeto de alguma classe "concreta"
       relacionada ao Freemind.

       Argumentos
       -----------

       xml_content é o conteúdo do mapa mental em formato string.

       Exceções
       ---------

       UnsupportedVersionException - lançada caso nenhuma classe dê suporte à
       versão do Freemind utilizada para criar o mapa mental. A checagem de
       suporte à versão precisa ser repetida neste nível porque pode haver um
       esquema RelaxNG, mas as operações podem não estar implementadas na
       hierarquia de classes do gerador.

    """
    base_class = BaseFreemind(xml_content)
    self._map_version = base_class.extract_map_version()

    try:
      cls_object = self._search_concrete_class()
      self._freemind_instance = cls_object(xml_content)

    except UnsupportedVersionException, exception:
      raise exception.__class__(exception.message)


  def _extract_graph_node_attributes(self, xml_node):
    """Retorna os dados que devem ser atribuídos a um nó no grafo.

       Argumentos
       -----------

       xml_node é o nó a ser analisado.

    """
    # Para saber como extrair os dados do nó é necessário conhecer seu tipo.
    node_type = BaseFreemind.guess_node_type(xml_node)
    node_data = None

    if node_type == LinkNode.TYPE:
      node_data = GenericNode.has_structure(BaseFreemind.extract_node_text(xml_node), LinkNode.GLOBAL_STRUCTURE).groupdict()
    elif node_type == InfoNode.TYPE:
      node_data = GenericNode.has_structure(BaseFreemind.extract_node_text(xml_node), InfoNode.GLOBAL_STRUCTURE).groupdict()
    else:
      node_data = GenericNode.has_structure(BaseFreemind.extract_node_text(xml_node), StepNode.GLOBAL_STRUCTURE).groupdict()
      node_data['notes'] = self._freemind_instance.extract_comments(xml_node)

    return node_data


  def _depth_first_builder(self, xml_parent_node, target_graph, graph_parent_node):
    """Constrói o grafo correspondente ao cenário/caso de uso do mapa mental.

       Argumentos
       -----------

       xml_parent_node é o nó XML em relação ao qual são realizadas as operações.

       target_graph é o grafo no qual são adicionados os vértices e as arestas.

       graph_parent_node é o nó do grafo no qual serão adicionados os filhos encontrados.

    """
    children = [node for node in xml_parent_node.iterchildren(tag = 'node')]

    for child in children:
      graph_node_attrs = self._extract_graph_node_attributes(child)
      # Não adiciona o nó se for um link.
      if 'link_reference' not in graph_node_attrs.keys():
        next_node_number = len(target_graph.nodes())
        target_graph.add_node(next_node_number, data = {key:value.strip() for key,value in graph_node_attrs.items()})
        target_graph.add_edge(graph_parent_node, next_node_number)
        self._depth_first_builder(child, target_graph, next_node_number)


  def build_graphs(self):
    """Constrói um grafo para cada cenário/caso de uso existente no mapa mental."""
    self._graph_list = []
    scenario_list = self._freemind_instance.extract_scenarios()

    for scenario in scenario_list:
      # Extrai os dados do caso de uso para adicionar como dados do primeiro nó do grafo.
      scenario_data = GenericNode.has_structure(BaseFreemind.extract_node_text(scenario), UCNode.GLOBAL_STRUCTURE)

      # Cria o grafo, adicionando os dados do cenário/caso de uso no primeiro
      # nó (raiz) e adiciona os demais nós recursivamente, utilizando busca em
      # profundidade.
      self._graph_list.append(ScenarioGraph(scenario_data.groupdict()))
      self._depth_first_builder(scenario, self._graph_list[-1], 0)


  def _build_context_data(self, graph, action_path):
    """Constrói a estrutura que armazena os dados que serão utilizados no
       contexto do template do XML.

       Argumentos
       -----------

       graph é o grafo a ser processado.

       action_path é a lista de nós (caminho) que será processada para gerar
       a estrutura contendo os dados do roteiro.

    """
    full_scenario = {}
    aux_action_list = []

    # Obtém as informações gerais do cenário/caso de uso, armazenadas por padrão
    # no nó 0 (zero).
    full_scenario.update(graph.get_node_info()[0]['data'])

    for node in action_path:
      node_data = graph.get_node_info(node)[0]['data']
      # Se o nó for do tipo INFO, concatenar o texto complementar ao nome do
      # caso de uso/cenário.
      # Se o nó for um PASSO, inserir o dicionário numa lista auxiliar que
      # conterá todas as ações.
      if 'infotext' in node_data.keys():
        full_scenario['name'] = ' / '.join([full_scenario['name'], node_data['infotext']])
      else:
        aux_action_list.append(node_data)

    full_scenario['action_list'] = aux_action_list
    return full_scenario


  def build_good_xml(self):
    """Percorre o grafo já validado e constrói o XML dos casos de teste."""
    scenario_list = []
    for graph in self._graph_list:
      # Obter as folhas do grafo.
      leaf_nodes = graph.leaves()

      # Para cada folha obter o gerador de caminhos independentes.
      independent_paths_generators = [networkx.all_simple_paths(graph, 0, leaf) for leaf in leaf_nodes]

      for path_generator in independent_paths_generators:
        while True:
          try:
            current_path = path_generator.next()
            current_path.remove(0)
            testcase_data = self._build_context_data(graph, current_path)
            scenario_list.append(testcase_data)
          except StopIteration:
            break

    template = get_template('gerador_roteiros/generic_template.xml')
    context = Context({'validation_status': True, 'scenario_list': scenario_list})
    return template.render(context)


  def validate(self):
    """Contém uma sequência de validações necessárias antes que o grafo seja
       montado.

    """
    try:
      # -- Nós em branco --
      # Exceções lançadas: EmptyNodesException
      self._freemind_instance.search_for_blank_nodes()

      # -- Verificação dos tipos dos nós --
      # Exceções lançadas: NodeTypeException
      self._freemind_instance.scenarios_extra_validations()
      self._freemind_instance.common_nodes_extra_validations()

      # -- Verificação da unicidade dos números de sequência em um caso de uso/cenário  --
      # Exceções lançadas: InvalidSequenceException
      scenario_list = self._freemind_instance.extract_scenarios()
      self._freemind_instance.has_repeated_sequence(scenario_list)

      # -- Verificação de link referenciando passo inexistente --
      # Exceções lançadas: UndefinedReferenceException
      self._freemind_instance.has_broken_links(scenario_list)

    except (EmptyNodeException, NodeTypeException, UndefinedReferenceException, InvalidSequenceException), exception:
      raise exception.__class__(exception.message)