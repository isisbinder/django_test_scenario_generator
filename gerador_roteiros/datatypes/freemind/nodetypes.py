# -*- coding: utf-8 -*-

"""
   datatypes.freemind.nodetypes
   ~~~~~~~~~

   Contém as classes que definem os tipos de nós suportados pelo Freemind.

   Created: 20/08/2012
   :copyright: (c) Ísis Binder, 2012 at COPEL

"""

import re

class GenericNode(object):
    """
       datatypes.freemind.nodetypes.GenericNode
       ~~~~~~~~~~

       Contém as operações genéricas para os nós comuns do mapa mental.

    """

    @staticmethod
    def has_structure(node_content, regex_pattern):
        """
            Verifica se o conteúdo do nó xml do mapa mental combina com um
            padrão de expressões regulares.

            Argumentos
            -----------

            node_content é o texto (string) do nó.

            regex_pattern é o padrão de expressão regular a ser utilizado na
            verificação/extração dos dados.

        """
        re_match = re.match(regex_pattern, node_content, re.MULTILINE | re.DOTALL | re.UNICODE | re.IGNORECASE)
        return re_match



class UCNode(GenericNode):
    """
       datatypes.freemind.nodetypes.UCNode
       ~~~~~~~~~~

       Contém as operações e definições para os nós do tipo CASO DE USO, que devem
       seguir um template de construção de texto.

    """
    #GLOBAL_STRUCTURE =  r'UC:\s*(.+)\sRequisitos:\s*(.+?)(?:\sPr.-condi..es:\s*(.+))?\sP.s-condi..es:\s*(.+)'
    REQUIRED_KEYS = ['name', 'requirements', 'postconditions']
    GLOBAL_STRUCTURE =  r'UC:\s*(?P<name>.+)\sRequisitos:\s*(?P<requirements>.+?)(?:\sPr.-condi..es:\s*(?P<preconditions>.+))?\sP.s-condi..es:\s*(?P<postconditions>.+)'
    TYPE = 'scenario'



class StepNode(GenericNode):
    """
       datatypes.freemind.nodetypes.StepNode
       ~~~~~~~~~~

       Contém as operações e definições para os nós do tipo PASSO, que devem
       seguir um template de construção de texto.

    """
    #GLOBAL_STRUCTURE = 'Sequ.ncia:\s*(.+)\sAtor:\s*(Usu.rio|Sistema)\sA..o:\s*(.+)'
    REQUIRED_KEYS = ['step_reference', 'actor', 'action_text']
    GLOBAL_STRUCTURE = r'Sequ.ncia:\s*(?P<step_reference>.+)\sAtor:\s*(?P<actor>(Usu.rio|Sistema))\sA..o:\s*(?P<action_text>.+)'
    TYPE = 'step'



class InfoNode(GenericNode):
    """
       datatypes.freemind.nodetypes.InfoNode
       ~~~~~~~~~~

       Contém as operações e definições para o nó INFO, cujo texto é
       complementar ao nome do cenário/caso de uso.

    """
    GLOBAL_STRUCTURE = r'(?P<infotext>.+)'
    INFO_ICON_NAME = 'info'
    TYPE = 'info'



class LinkNode(object):
    """
       datatypes.freemind.nodetypes.LinkNode
       ~~~~~~~~~~

       Contém as operações e definições para o nó LINK, cujo texto referencia
       um outro nó do tipo PASSO dentro de um mesmo cenário/caso de uso.

    """
    GLOBAL_STRUCTURE = r'(?P<link_reference>.+)'
    LINK_ICON_NAME = 'forward'
    TYPE = 'link'