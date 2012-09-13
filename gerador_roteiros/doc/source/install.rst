Instalação
===========

O gerador de roteiros depende dos seguintes pacotes Python:

* Python 2.7
* Django 1.4
* BeautifulSoup 3.2.1
* Lxml 2.3.5
* Numpy 1.6.2
* Networkx 1.7



Preparação do ambiente
----------------------

Para instalar o servidor Flask é necessário ter o interpretador Python instalado. Ele pode ser baixado através do link http://python.org/ftp/python/2.7.3/python-2.7.3.msi .

.. warning:: Mesmo que seu computador seja de 64bits, utilize a versão 32bits do interpretador, pois podem ocorrer problemas durante a instalação de um pacote para o qual só exista versão 32bits.


Baixe o instalador e execute-o com os valores fornecidos por padrão. Ao concluir a instalação do interpretador Python, você deve abrir o Painel de Controle do Windows e 
entrar em "Sistema". Já com a janela de opções de configuração do sistema aberta, selecione a aba "Configurações avançadas do sistema" e clique no botão "Variáveis de ambiente".
Aqui informaremos ao Windows onde o Python foi instalado.

Na janela de variáveis do ambiente existem dois grupos, o de variáveis para o usuário e o de variáveis globais do sistema. Execute os seguintes passos no segundo grupo:

#. Selecione a opção para criar uma nova variável;
#. Dê a ela o nome **PYTHONPATH** e coloque como valor a string *C:\Python27;C:\Python27\Lib;C:\Python27\Scripts*, supondo que *C:\Python27* é o diretório de instalação do interpretador;
#. Clique em OK;
#. Localize a variável **Path**, selecione-a e clique em "Editar";
#. No final do conteúdo da variável, adicione o texto *;%PYTHONPATH%* e clique em OK;
#. Clique em OK nas demais janelas para aplicar as alterações

Para verificar se o Windows reconhece o interpretador como um comando, abra o prompt de comando e digite :command:`python --version` (são dois hífens). Deve ser impressa a versão instalada do interpretador Python.

Após a instalação do interpretador é necessário instalar as ferramentas para realizar a instalação das dependências da aplicação, pois a versão para Windows não vem com elas embutidas no instalador.
Abra o link http://pypi.python.org/pypi/setuptools#files e baixe o instalador Windows do pacote **setuptools** para a versão do Python instalada em seu computador. 
Execute-o normalmente com as opções padrão.     


Instalação das dependências
---------------------------

.. note::
  Se estiver atrás de um proxy, para que a instalação das dependências através da Internet funcione com o *easy_install*, é necesário especificar uma variável de usuário chamada **http_proxy**, 
  no formato *http://[USUARIO]:[SENHA_DE_REDE]@[IP_PROXY]:[PORTA_PROXY]*.
  

Ao invés de baixar todas as dependências com o *easy_install* (gerenciador de pacotes Python), todas elas serão instaladas a partir da máquina local. Para isso, baixe os seguintes pacotes seguindo 
a versão do Python instalada. Os pacotes podem ter a forma de um instalador *msi/exe*, um arquivo compactadado *tar.gz* ou *zip* ou um arquivo conhecido como *Python egg* com a extensão *egg*.

* BeautifulSoup (http://pypi.python.org/pypi/BeautifulSoup/3.2.1)
* Lxml (http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)
* Numpy (http://pypi.python.org/pypi/numpy/1.6.2#downloads)
* Networkx (http://pypi.python.org/pypi/networkx/1.7)
* Django (https://www.djangoproject.com/download/1.4.1/tarball/)

O processo de instalação é simples: apenas execute o comando :command:`easy_install [CAMINHO_ABSOLUTO DO ARQUIVO]`. Por exemplo: :command:`easy_install "C:\\Documents and Settings\\c050960\\Downloads\\BeautifulSoup3.2.1.tar.gz"`.
Todos os formatos de arquivos mencionados anteriormente podem ser instalados utilizando esse comando.