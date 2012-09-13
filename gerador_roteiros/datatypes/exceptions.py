# -*- coding: utf-8 -*-
"""
  gerador_roteiros.datatypes.exceptions
  ~~~~~~~~~~

  Contém exceções personalizadas para serem utilizadas pelo gerador de roteiros.

  Created: 27/08/2012

"""
class RelaxNGValidationException(Exception):
  """
    gerador_roteiros.datatypes.exceptions.RelaxNGValidationException
    ~~~~~~~~~~

    Esta exceção deve ser lançada somente durante a etapa de validação com o
    esquema RelaxNG.

  """
  def __init__(self, message):
    super(RelaxNGValidationException, self).__init__(message)



class UnsupportedVersionException(Exception):
  """
    gerador_roteiros.datatypes.exceptions.UnsupportedVersionException
    ~~~~~~~~~~

    Esta exceção deve ser lançada somente se for detectada uma versão do
    Freemind que não possui suporte do gerador de roteiros.

  """
  def __init__(self, message):
    super(UnsupportedVersionException, self).__init__(message)


class EmptyNodeException(Exception):
  """
    gerador_roteiros.datatypes.exceptions.EmptyNodeException
    ~~~~~~~~~~

    Esta exceção deve ser lançada somente se houver nós sem texto dentro do
    mapa mental.

  """
  def __init__(self, message):
    super(EmptyNodeException, self).__init__(message)


class NodeTypeException(Exception):
  """
    gerador_roteiros.datatypes.exceptions.NodeTypeException
    ~~~~~~~~~~

    Esta exceção deve ser lançada somente se o tipo do nó for indefinido.

  """
  def __init__(self, message):
    super(NodeTypeException, self).__init__(message)



class UndefinedReferenceException(Exception):
  """
    gerador_roteiros.datatypes.exceptions.UndefinedReferenceException
    ~~~~~~~~~~

    Esta exceção deve ser lançada somente se existirem links apontando para
    passos cujo número de sequência não existe dentro do caso de uso.

  """
  def __init__(self, message):
    super(UndefinedReferenceException, self).__init__(message)



class CyclicGraphException(Exception):
  """
     gerador_roteiros.datatypes.exceptions.CyclicGraphException
     ~~~~~~~~~~

     Esta exceção deve ser lançada somente se existirem ciclos no grafo do
     mapa mental.

  """
  def __init__(self, message):
    super(CyclicGraphException, self).__init__(message)



class InvalidSequenceException(Exception):
  """
     gerador_roteiros.datatypes.exceptions.InvalidSequenceException
     ~~~~~~~~~~

     Esta exceção deve ser lançada somente se existirem números de sequência
     repetidos dentro de um caso de uso/cenário.

  """
  def __init__(self, message):
    super(InvalidSequenceException, self).__init__(message)