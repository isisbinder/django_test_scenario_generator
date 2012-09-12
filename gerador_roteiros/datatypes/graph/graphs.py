# -*- coding: utf-8 -*-
"""
   datatypes.graph.graphs
   ~~~~~~~~~~

   Definição do tipo Grafo adaptado às necessidades da geração de roteiros.

   Created: 16/08/2012
   :copyright: (c) Ísis Binder, 2012 at COPEL

"""
import networkx

class ScenarioGraph(networkx.MultiDiGraph):
  """
     datatypes.graph.graphs.ScenarioGraph
     ~~~~~~~~~~

     Esta classe herda as propriedades da classe networkx.MultiDiGraph e
     acrescenta outras operações para que seja possível extrair dados
     relevantes para a geração de roteiros.

  """
  def __init__(self, scenario_data = {}):
    """Inicialização do objeto.

       Argumentos
       -----------

       scenario_data contém os dados do cenário cujo grafo deve ser criado. Por
       padrão recebe um dicionário vazio. Esta forma de argumento possibilita a
       execução da verificação de ciclos no grafo, pois existe uma chamada ao
       inicializador da classe sem argumentos. Caso o parâmetro scenario_data
       não possua valor padrão, ocorre um erro de número de argumentos.

    """
    super(ScenarioGraph, self).__init__()
    if scenario_data:
      self.name = scenario_data['name'].strip()
      self.add_node(0, data = scenario_data)



  def leaves(self):
    """Retorna os nós folha (não tem arestas de saída) do grafo."""
    return [node for node in self.nodes() if not self.out_degree(node)]


  def locate_link_target_index(self, mindmap_reference):
    """Localiza no grafo o índice (ou label) do nó correspondente ao número de
       sequência do mapa mental.

       Argumentos
       -----------

       mindmap_reference é o número de sequência do passo dentro do mapa mental.

    """
    # Obtém os nós do tipo PASSO (verificação do tipo por presença de chave).
    graph_step_nodes = [node_tuple for node_tuple in self.nodes(data = True) if 'step_reference' in node_tuple[1]['data'].keys()]

    # Filtra a lista de nós PASSO para que seja localizado somente o nó cujo
    # número de sequência corresponda à sequência passada como argumento.
    reference_index = filter(lambda node_tuple: node_tuple[1]['data']['step_reference'] == mindmap_reference, graph_step_nodes)[0]

    return reference_index[0]


  def get_node_info(self, node_index = 0):
    """Retorna as informações contidas no nó passado como argumento. Por padrão,
       este método retorna as informações do caso de uso/cenário, contidas no
       nó zero.

       Argumentos
       -----------

       node_index é o índice (ou label) do nó que terá suas informações extraídas.

    """
    return [node_tuple[1] for node_tuple in self.nodes(data = True) if node_tuple[0] == node_index]