# -*- coding: utf-8 -*-
"""
   datatypes.freemind.basefreemind
   ~~~~~~~~~~

   Contém a classe básica para implementação das funcionalidades de extração
   dos dados do mapa mental.

   Created: 16/08/2012

"""

from collections import Counter
from lxml import etree
import BeautifulSoup
from gerador_roteiros.datatypes.freemind.nodetypes import *
from gerador_roteiros.datatypes.exceptions import EmptyNodeException, NodeTypeException, UndefinedReferenceException, InvalidSequenceException


class BaseFreemind(object):
  """
     datatypes.freemind.basefreemind.BaseFreemind
     ~~~~~~~~~~

     Classe genérica com operações comuns a diferentes versões do Freemind.
     Caso seja necessário, elas podem ser sobrescritas por classes filhas para
     tratar particularidades de uma determinada versão.

  """



  @staticmethod
  def _has_special_icon(xml_node):
    """Verifica se o nó XML possui ícones especiais, retornando seu nome
       ou None caso não possua nenhum ícone especial.

       Argumentos
       -----------

       xml_node é o elemento XML a ser analisado.

    """
    #
    # PROCESSO DE VERIFICAÇÃO:
    # 1- Obtém-se os filhos diretos de nome/tag 'icon' do nó informado como
    # argumento.
    # NOTE: Não foi utilizada a construção list(xml_node.iterchildren(tag = 'icon'))
    # porque no caso do mapa info_com_estrutura_passo.mm ela não detectava o
    # ícone.
    icons_list = filter(lambda elem: 'icon' in elem.tag, xml_node.getchildren())
    icon_builtin_names = [icon.xpath('@BUILTIN')[0] for icon in icons_list]

    # 2- Dependendo do nome do ícone, define-se o tipo do nó.
    node_type = None
    if InfoNode.INFO_ICON_NAME in icon_builtin_names:
      node_type = InfoNode.INFO_ICON_NAME

    elif LinkNode.LINK_ICON_NAME in icon_builtin_names:
      node_type = LinkNode.LINK_ICON_NAME

    return node_type



  @staticmethod
  def _combine_graphic_structural_types(graphic_type, structural_type):
      """Baseado no suposto tipo de nó detectado através da verificação de
         ícones especiais e estrutura do texto, retorna o tipo de nó verdadeiro
         de um nó comum (os que vem após os casos de uso).

         Caso graphic_type e structural_type sejam diferentes, o tipo retornado
         será None. Porém, como estamos lidando com informações que pertencem a
         um caso de uso, se o tipo estrutural for "scenario", será retornado o
         tipo None (indeterminado).

         Argumentos
         -----------

         graphic_type é o tipo do nó definido de acordo com os ícones associados.

         structural_type é o tipo do nó definido a partir da estrutura de seu texto.
         Não pode ter o valor "scenario", pois esta validação é realizada em
         nós pertencentes a um caso de uso.

      """
      # Se houver um tipo definido pelo ícone associado ao nó, então espera-se
      # que não haja nenhum padrão estrutural de texto nele. Isso acontece para
      # os nós LINK e INFO. Nesse caso, o tipo do nó é definido pelo ícone
      # associado.
      if graphic_type and not structural_type:
         return graphic_type

      # Se não houver um ícone especial associado ao nó e houver um tipo estrutural
      # definido por texto, então a estrutura do texto define o tipo do nó.
      # ATENÇÃO: como não pode haver nós contendo texto de caso de uso/cenário
      # dentro de um caso de uso, é necessário explicitar isso no IF. Nesse caso
      # o tipo do nó será  None.
      if not graphic_type and structural_type and structural_type != UCNode.TYPE:
         return structural_type

      return None



  @staticmethod
  def _guess_type_by_text(xml_node):
    """Baseado na estrutura do texto principal do nó, retorna seu tipo
       (PASSO ou CASO DE USO).

       Argumentos
       -----------

       xml_node é o elemento XML que terá seu conteúdo analisado.

    """
    for possible_types in [StepNode, UCNode]:
      if GenericNode.has_structure(BaseFreemind.extract_node_text(xml_node), possible_types.GLOBAL_STRUCTURE):
        return possible_types.TYPE
    return None




  @staticmethod
  def guess_node_type(xml_node):
      """Verifica qual o tipo do nó sendo analisado.
         A análise está dividida em 2 partes: a primeira leva em conta os ícones
         que o nó XML possui, e a segunda, a estrutura do texto principal.
         Após as duas análises, realiza-se uma combinação de seus resultados para
         determinar o tipo verdadeiro do nó.

         Casos inválidos não cobertos pela validação com RelaxNG:
               - Último PASSO com ícone LINK

         Argumentos
         -----------

         xml_node é o elemento XML que será analisado.

      """
      graphic_type, structural_type, final_node_type = None, None, None

      # 1- Verifica o tipo definido pelo ícone especial.
      special_icon_name = BaseFreemind._has_special_icon(xml_node)
      if special_icon_name == LinkNode.LINK_ICON_NAME:
          graphic_type = LinkNode.TYPE

      elif special_icon_name == InfoNode.INFO_ICON_NAME:
          graphic_type = InfoNode.TYPE

      # 2- Verifica o tipo baseado na estrutura do texto.
      structural_type = BaseFreemind._guess_type_by_text(xml_node)

      # 3- Determina o tipo verdadeiro do nó combinando os dois tipos anteriores.
      final_node_type = BaseFreemind._combine_graphic_structural_types(graphic_type, structural_type)

      return final_node_type





  @staticmethod
  def extract_common_nodes_by_type(scenario_node, node_type = StepNode.TYPE):
    """Extrai todos os nós (tag NODE) de um determinado tipo para um certo caso de uso.

       Argumentos
       -----------

       scenario_node é o elemento xml representando o cenário/caso de uso
       para o qual será realizada a extração.

       node_type determina o tipo de nó que será extraído.

    """
    all_nodes = scenario_node.iterdescendants(tag = 'node')
    return [node for node in all_nodes if BaseFreemind.guess_node_type(node) == node_type]



  @staticmethod
  def extract_node_text(xml_node):
    """Extrai o texto principal do nó.

       Argumentos
       -----------

       xml_node é o elemento XML cujo texto será extraído.

    """
    return xml_node.xpath("@TEXT")[0]



  def __init__(self, mindmap_content):
    """Inicializador da classe. Apenas transforma a string em um documento XML.

       Argumentos
       -----------

       mindmap_content é uma string a partir da qual será criado um
       documento XML.

    """
    self._mindmap_content = etree.fromstring(mindmap_content)



  def extract_map_version(self):
    """Extrai a versão do Freemind utilizada na criação do mapa mental."""
    return self._mindmap_content.xpath('/map/@version')[0]




  def extract_scenarios(self):
    """Extrai todos os nós de cenário do mapa mental."""
    return self._mindmap_content.xpath('/map/node')[0].getchildren()



  def extract_comments(self, xml_node):
    """Retorna os comentários do nó.

       Argumentos
       -----------

       xml_node é o elemento XML a ser processado.

    """
    comment_list = xml_node.xpath('richcontent/html/body/*')
    comments = ''.join([node.text for node in comment_list])
    comments = BeautifulSoup.BeautifulSoup(comments).getText()
    return comments




  def search_for_blank_nodes(self):
    """Pesquisa por nós cujo texto está em branco.

       Exceções
       ---------

       EmptyNodeException - Lançada se o mapa possui nós sem texto.

    """
    nodes = list(self._mindmap_content.xpath('/map')[0].iterdescendants(tag = 'node'))
    node_text = [BaseFreemind.extract_node_text(node) for node in nodes]
    if node_text.count(''):
      raise EmptyNodeException('Existem nós em branco no mapa mental.')



  def scenarios_extra_validations(self):
    """Executa diversos testes (não cobertos pelas validações anteriores)
       para validar os nós do tipo Caso de Uso/Cenário.
       Neste ponto já foi verificado que nenhum nó do mapa mental está com o
       atributo TEXT vazio, portanto, é seguro utilizar expressões regulares
       sem acumular responsabilidades.

       Exceções
       ----------

       NodeTypeException - lançada caso os cenários não sigam a estrutura
       convencionada.

    """
    # Alvo da primeira validação extra: nós de cenário/caso de uso.
    # Como a análise de texto vazio já foi feita, as únicas possibilidades
    # neste ponto de execução são:
    # 1- Ter uma estrutura de escrita diferente do proposto;
    # 2- Ter estrutura incompleta (não possuir atributos obrigatórios);
    # 3- Ser um nó válido.

    # Comparar com expressão regular para verificar estrutura.
    regex_matches = [GenericNode.has_structure(BaseFreemind.extract_node_text(scenario), UCNode.GLOBAL_STRUCTURE) for scenario in self.extract_scenarios()]

    # Se algum dos nós resultar em match = None, então marca-se o mapa como inválido.
    if not all(regex_matches):
      raise NodeTypeException("Existem nós de caso de uso que não seguem o padrão de escrita.")

##    # Se o match for diferente de None, mas não houver pelo menos as chaves
##    # 'name', 'reqs' e 'posc', então o nó é inválido.
##    # TODO Encontrar uma construção de mapa mental que justifique este código. Caso contrário, remover.
##    for match in regex_matches:
##      if not set(UCNode.REQUIRED_KEYS).issubset(set(match.groupdict().keys())):
##        raise RequiredAttributesException("Existem nós de caso de uso que não possuem atributos obrigatórios (UC, Requisitos, Pós-condições)")





  def common_nodes_extra_validations(self):
    """Executa diversos testes para o restante dos nós (comuns), validando os
       nós PASSO, LINK e INFO.
       Neste ponto já foi verificado que nenhum nó do mapa mental está com o
       atributo TEXT vazio, portanto, é seguro utilizar expressões regulares
       sem acumular responsabilidades.

       Exceções
       ---------

       NodeTypeException - lançada somente quando o tipo determinado pelos ícones
       associados ao nó conflita com o tipo determinado por sua estrutura de texto.

    """
    # Alvo da segunda validação extra: nós comuns.
    # Como todos os nós abaixo dos casos de uso são tratados como nós comuns,
    # a validação é diferente daquela realizada para os casos de uso,
    # considerando os ícones associadaos ao nó e seu texto principal.
    # Como a análise de texto vazio já foi feita, as únicas possibilidades
    # neste ponto de execução são:
    # 1- Ter uma estrutura de escrita diferente do proposto;
    # 2- Ter estrutura incompleta (não possuir atributos obrigatórios);
    # 3- Ser um nó válido.

    scenario_list = self.extract_scenarios()
    for scenario in scenario_list:
      for common_node in list(scenario.iterdescendants(tag = 'node')):
        node_type = BaseFreemind.guess_node_type(common_node)

        if not node_type:
          raise NodeTypeException("Existem nós que não seguem o padrão de escrita.")

##        # Caso o tipo detectado tenha sido PASSO, ainda é necessário verificar
##        # se ele possui todos os atributos obrigatórios preenchidos.
##        # TODO Pensar em um caso para exercitar o código abaixo. Caso contrário, remover.
##        if node_type == StepNode._TYPE:
##          regex_match = GenericNode.has_structure(BaseFreemind._extract_node_text(common_node), StepNode.GLOBAL_STRUCTURE)
##
##          if set(regex_match.groupdict()) != set(StepNode.REQUIRED_KEYS):
##            raise RequiredAttributesException("Existem passos com campos obrigatórios ausentes.")




  def has_repeated_sequence(self, scenario_list):
    """Para cada cenário, verifica se existem passos com número de sequência
       repetido.

       Argumentos
       -----------

       scenario_list é a lista de cenários/casos de uso do mapa mental.


       Exceções
       ---------

       InvalidSequenceException - lançada somente se o mapa possuir passos com
       sequência repetida dentro de um mesmo caso de uso/cenário.

    """
    for scenario in scenario_list:
      sequence_numbers_found = []
      scenario_step_nodes = BaseFreemind.extract_common_nodes_by_type(scenario)
      for step in scenario_step_nodes:
        step_data = GenericNode.has_structure(BaseFreemind.extract_node_text(step), StepNode.GLOBAL_STRUCTURE).groupdict()
        sequence_numbers_found.append(step_data['step_reference'])

      step_sequence_count = Counter(sequence_numbers_found).values()
      if any(map(lambda count: count > 1, step_sequence_count)):
        raise InvalidSequenceException("Existem casos de uso com repetição do número de sequência em passos.")



  def has_broken_links(self, scenario_list):
    """Verifica a consistência dos links em uma lista de cenários/casos de uso para
       que não ocorram links referenciando passos não existentes.

       Argumentos
       ---------

       scenario_list é a lista de casos de uso contidos no mapa mental.

    """

    for scenario in scenario_list:
      # Para cada cenário/caso de uso realiza uma busca pelos nós do tipo LINK e
      # do tipo PASSO.
      scenario_link_nodes = BaseFreemind.extract_common_nodes_by_type(scenario, LinkNode.TYPE)
      scenario_step_nodes = BaseFreemind.extract_common_nodes_by_type(scenario)

      # Para cada LINK extrai o texto que corresponde ao número de sequência do
      # passo referenciado.
      link_references = [BaseFreemind.extract_node_text(node) for node in scenario_link_nodes]

      # Para cada PASSO extrai seu número de sequência.
      step_number = [GenericNode.has_structure(BaseFreemind.extract_node_text(node), StepNode.GLOBAL_STRUCTURE).groupdict()['step_reference'] for node in scenario_step_nodes]

      # Se a diferença entre o conjunto de links e o de passos não resultar em
      # um conjunto vazio*, então existem links que apontam para passos inexistentes.
      # * A diferença entre dois conjuntos, A-B, resulta num conjunto de elementos
      # presentes em A e ausentes em B.
      if set(link_references) - set(step_number):
         raise UndefinedReferenceException("O mapa mental possui casos de uso com links que referenciam passos inexistentes.")