Introdução
==========

O processo de teste é visto, comumente, como apenas a execução de um programa visando encontrar defeitos.
Porém, existem atividades antes e depois da execução do programa que também fazem parte da atividade de teste.

Uma dessas atividades é a modelagem de teste, na qual os casos de testes e seus respectivos dados são especificados e criados.
Segundo o ISTQB, um caso de teste consiste de um conjunto de valores de entrada, pré-condições, resultados de execução e pós-condições. 
Os resultados esperados incluem as saídas, mudanças de dados e status e qualquer outra consequência do teste, devendo ser definido antes da execução do mesmo.

A equipe de teste da COPEL, formada em 2008, tem como objetivo prezar pela qualidade do produto, realizando validações de requisitos e modelando os casos de teste
a serem executados como fluxos de ações dentro da aplicação. Para facilitar a visualização, a equipe utiliza uma ferramenta para criação de mapas mentais gratuita, 
o Freemind. Após a modelagem dentro do Freemind, o analista copia todo o fluxo e seus dados complementares para dentro do gerenciador de testes desenvolvido pela 
equipe para, então, dar início à execução dos roteiros.

Problemas desse procedimento:

* É cansativo;
* O roteiro pode não refletir o mapa e vice-versa;
* É demorado

Como a atividade que mais consome esforço é a criação do mapa mental, desenvolveu-se uma solução que permite a geração de roteiros de teste baseados no mapa mental.
Através dela é possível criar uma cópia fiel ao mapa mental, reduzindo drasticamente o esforço da operação, pois a maior parte do tempo será dispendida na análise 
dos documentos e processos ao invés da adequação do texto para o GTeste.