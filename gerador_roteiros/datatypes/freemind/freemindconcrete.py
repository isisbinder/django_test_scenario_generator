# -*- coding: utf-8 -*-
"""
    datatypes.freemind.freemindconcrete
    ~~~~~~~~~~

    Contém as classes concretas para cada versão do Freemind suportada pela
    aplicação. Isso é necessário caso o XML seja alterado de uma versão para outra.

    Created: 20/08/2012

"""

from gerador_roteiros.datatypes.freemind.basefreemind import BaseFreemind

class FreemindPadrao(BaseFreemind):
      """
         datatypes.freemind.freemindconcrete.FreemindPadrao
         ~~~~~~~~~~

         Classe padrão para utilização no processamento do mapa mental.
         Abrange as seguintes versões do aplicativo:
         - 0.9.0

      """

      _versions = ['0.9.0']

      def __init__(self, mindmap_content):
          super(FreemindPadrao, self).__init__(mindmap_content)