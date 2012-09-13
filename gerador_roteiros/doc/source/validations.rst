Detalhes da validação dos mapas mentais
========================================

Apesar da sintaxe do mapa mental ser relativamente simples, antes de convertê-lo em roteiros de teste, é necessário validá-lo.
Para isso utilizou-se validações em etapas, com grau de complexidade variado.


1ª etapa -- RelaxNG
--------------------

O RelaxNG é uma linguagem de esquema para XML desenvolvida pela OASIS (Advancing Open Standards for the Information Society), 
semelhante ao XSD do World Wide Web Consortium (W3C).
Ambas são padrões ISO, mas a escolha pelo RelaxNG se deve à maior facilidade de compreensão.

O que esta etapa faz é verificar se o documento é bem-formado, ou seja, segue determinadas regras de sintaxe especificadas no arquivo de esquema.
Existem algumas limitações observadas na validação com esquemas XML que foram implementadas em outras etapas:

#. Não verifica se o nó está em branco. Independente do texto estar em branco (string vazia) ou não, o validador acusa corretamente a presença de uma string.
#. Não verifica se o nó possui a estrutura correta para ser distinguido entre PASSO ou CASO DE USO;
#. Se existir um nó INFO sem filho, a validação acaba trantando-o como LINK com filho;

Caso alguma regra de sintaxe especificada no esquema seja violada, a aplicação retorna uma exceção e cria um XML descrevendo o 
resultado da validação copiando as mensagens de log do validador RelaxNG. Como não é possível programar dentro do esquema, essas 
mensagens podem dizer pouca coisa, mas ainda assim evitam que o mapa mental inválido seja convertido em roteiros. Na dúvida, revise 
o mapa mental.


2ª etapa -- Versão do Freemind
--------------------------------

Após validar a estrutura do mapa mental, é necessário verificar se o gerador sabe como tratar os dados do mapa. O motivo para a 
criação dessa etapa são as diferenças encontradas entre a versão 0.8 (usada anteriormente) e a 0.9. A mais marcante é a representação 
de notas (comentários): na versão 0.8 o texto fazia parte de uma tag <node type="NOTE">, enquanto que na versão 0.9 esse campo foi 
transformado em um richtext, contendo tags HTML.

A verificação consiste em extrair a versão da aplicação utilizada, informada na primeira tag do mapa mental, e procurar, em tempo 
de execução, a classe adequada para tratar o arquivo. Se houver diversas versões que produzem o mesmo XML, não é necessário escrever 
mais classes: existe uma variável nas classes "concretas" que informam quais versões elas são capazes de tratar. Caso nenhuma classe 
seja encontrada, o programa lança uma exceção e gera um XML informando que não existe implementação para tratar o arquivo gerado.

A primeira versão oficial do Freemind utilizada na criação deste gerador de roteiros é a 0.9.0.


3ª etapa - Validações extras
----------------------------- 

A terceira etapa da validação visa tratar os casos não cobertos na primeira etapa e consiste das seguintes validações extras:

#. Verificar se o nó contém texto;
#. Verificar se o nó possui a estrutura esperada;

É necessário que todos os nós tenham algum texto escrito, por isso a primeira "sub-validação".

A segunda "sub-validação" utiliza expressões regulares para verificar se o nó possui a estrutura convencionada para sua função. Os nós de 
caso de uso são determinados pela sua posição no mapa mental, vindo imediatamente após o nó central. Esses nós não podem ter outra 
estrutura de texto a não ser a especificada para nós do tipo "CASO DE USO". Como o esquema RelaxNG especifica que um nó "CASO DE USO" 
não pode possuir ícones INFO e LINK, estes são os únicos valores possíveis:

#. Estrutura de Caso de Uso;
#. Estrutura de Passo;
#. Sem estrutura (Link/Info)

Se os itens 2 e 3 forem detectados, o mapa é marcado como inválido.

Para os demais nós ("PASSO", "LINK" e "INFO"), essa validação é substituída pela verificação composta do tipo de nó, na qual são 
analisados os ícones associados ao nó e seu texto. Abaixo é apresentada uma tabela com as possíveis entradas e seus resultados.

+--------------------------+-----------------------------+---------------------------------------------+
|    TIPO DETERMINADO      |      TIPO DETERMINADO       |      TIPO DETERMINADO PELA                  |
|        PELO ÍCONE        |         PELO TEXTO          |     COMBINAÇÃO DOS ELEMENTOS                |
+==========================+=============================+=============================================+
|          Link            |            ---              |                Link                         |
+--------------------------+-----------------------------+---------------------------------------------+
|          Link            |            Passo            |           INVÁLIDO (None)                   |
+--------------------------+-----------------------------+---------------------------------------------+
|          Link            |         Caso de uso         |           INVÁLIDO (None)                   |
+--------------------------+-----------------------------+---------------------------------------------+
|          Info            |            ---              |                Info                         |
+--------------------------+-----------------------------+---------------------------------------------+
|          Info            |            Passo            |           INVÁLIDO (None)                   |
+--------------------------+-----------------------------+---------------------------------------------+
|          Info            |         Caso de uso         |           INVÁLIDO (None)                   |
+--------------------------+-----------------------------+---------------------------------------------+
|          ---             |           Passo             |         Passo (após nó UC)                  |
|                          |                             |      None (no lugar do nó UC)               |
+--------------------------+-----------------------------+---------------------------------------------+
|          ---             |         Caso de uso         |    Caso de uso (após nó central)            |
|                          |                             |        None (se após nó UC)                 |
+--------------------------+-----------------------------+---------------------------------------------+


4ª etapa -- Validação dos links e dos números de sequência
------------------------------------------------------------

Para evitar problemas na construção do grafo, após verificar toda a estrutura dos nós, o gerador verifica as seguintes propriedades:

#. Não podem existir passos com número de sequência repetidos dentro de um mesmo cenário/caso de uso;
#. Dentro de um cenário/caso de uso não pode haver links referenciando passos cujo número de sequência não existe.

Essa verificação é extremamente importante, pois a montagem do grafo se dá em duas partes: a primeira apenas copia os dados extraídos 
do mapa mental e a segunda substituí os nós do tipo LINK por arestas, ligando seu nó antecessor ao nó referenciado.


5ª etapa - Verificação de ciclos
---------------------------------

A última etapa antes da geração dos roteiros verifica se o grafo gerado a partir de cada caso de uso contém pelo menos um nó folha, 
indicando que existe uma sequência de passos que leva ao final do roteiro.