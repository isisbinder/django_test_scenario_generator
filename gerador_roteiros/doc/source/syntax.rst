Sintaxe do mapa mental
=======================

Esta parte da documentação visa detalhar o formato de cada tipo de nó reconhecido pelo gerador de roteiros.
É importante que os mapas mentais sejam escritos seguindo esta especificação, sob pena da aplicação não funcionar, já que o mapa será considerado inválido.



Nó principal
------------

O nó principal ou nó central do mapa mental é aquele imediatamente visível quando se cria um novo mapa. Como ele não é considerado para a elaboração dos roteiros, 
pode conter qualquer texto, mas o indicado é escrever o sistema para o qual o mapa será elaborado. Comentários sobre status do projeto, como sprint atual (no caso 
de projetos que utilizem metodologias ágeis), são aceitos.


Casos de uso
------------

O nó do tipo "caso de uso" é aquele nó filho do nó principal do mapa. Podem existir diversos casos de uso, e seu formato é como segue:

| UC: [nome do cenário]
| Requisitos: [lista de requisitos atendidos]
| Pré-condições: [lista de pré-condições para execução do cenário]
| Pós-condições: [lista de pós-condições]

.. note:: *Todos* os campos são obrigatórios, exceto o campo "pré-condições".

.. warning:: A lista dos requisitos deve ser preenchida utilizando-se o identificador dos requisitos no GTeste, separados por vírgula. **O programa não funciona com requisitos contendo espaços no nome.**



.. figure:: images\exemplo_uc.png
   :alt: Exemplo de nó do tipo "caso de uso".
   :align: center
   
   *Exemplo de nó do tipo "caso de uso".*

   
   
Pode-se inserir formatação de texto, comentários (notas) e ícones, desde que estes não sejam os ícones específicos para os nós dos tipos "link" e "info".


Passos
------

Os nós que especificam os passos do roteiro possuem o seguinte formato, sendo todos os campos obrigatórios:

| Sequência: [número de sequência dentro do caso de uso]
| Ator: (Usuário|Sistema)
| Ação: [descrição da ação]

A especificação do ator responsável pela ação descrita serve unicamente para classificar as ações e ordená-las durante a interpretação do XML de retorno dentro do GTeste.
Normalmente, um passo constitui-se do par (ação do usuário, resposta do sistema), mas é possível "quebrar" as ações dos dois atores. Neste caso, um elemento do par 
ficará vazio: (ação do usuário, --- ) (ação do usuário, resposta do sistema)  ou (ação do usuário, resposta do sistema) ( --- , resposta do sistema).



.. figure:: images\exemplo_passo.png
   :alt: Exemplo de nó do tipo "passo".
   :align: center
   
   *Exemplo de nó do tipo "passo".*

                 
   
Esses nós também podem ter texto formatado, comentários e ícones (exceto os específicos dos nós "link" e "info").

                              
Links
-----

Os links entre passos servem para reaproveitar textos, evitando que sejam copiados e colados novamente em outra parte do cenário. Sua sintaxe é mais simples, devendo 
conter **apenas** o número de sequência a partir do qual o fluxo se repete e um ícone específico.


.. figure:: images\exemplo_link.png
   :alt: Exemplo de nó do tipo "link".
   :align: center
   
   *Exemplo de nó do tipo "link".* 


.. warning:: Links não devem ter nós filhos.



Texto complementar (info)
--------------------------

Este nó possui um texto que será concatenado ao nome do cenário, devendo ter somente o ícone específico designado. Aceita formatação de texto e comentários.

.. figure:: images\exemplo_info.png
   :alt: Exemplo de nó do tipo "info".
   :align: center
   
   *Exemplo de nó do tipo "info".* 

.. warning:: Nós contendo texto complementar devem ter pelo menos 1 nó filho.


Restrições
----------

Além das restrições relacionadas aos ícones que podem ser inseridos em cada tipo de nó, existem restrições nos comentários. O Freemind gera uma página HTML quando se 
escreve alguma nota em algum nó (na janela na parte inferior do programa). Como seria trabalhoso especificar um documento de validação para o HTML gerado dentro do esquema 
de validação do mapa mental, optou-se por restringir os elementos que seriam aceitos nessa área. Atualmente são aceitos somente demarcações de parágrafos, ou seja, não 
se pode inserir formatação nem elementos como tabelas e listas numeradas.