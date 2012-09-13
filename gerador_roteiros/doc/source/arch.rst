Arquitetura e procedimento
===========================

A aplicação foi desenvolvida utilizando-se o framework web Python Django. Logo, a aplicação se compõe de duas partes: a desktop, escrita no Lazarus, e a parte web.
Antes de gerar os roteiros, a aplicação executa diversasa validações para que a conversão não seja realizada com erros ou pela metade.

Quando o analista conclui a elaboração do mapa mental, ele executa os seguintes passos:

#. Abrir o GTeste e realizar login;
#. Selecionar produto e versão;
#. Especificar requisitos da versão selecionada;
#. Criar um pedido para o produto e versão selecionados;
#. Selecionar o pedido correto e clicar com o botão direito sobre o mesmo;
#. Selecionar o item de menu referente à criação de roteiros via Freemind;
#. Indicar o caminho completo do arquivo do mapa mental
#. Solicitar geração dos roteiros.

O conteúdo do mapa mental será enviado através da rede para o servidor Django, que realizará a validação do mapa mental e o converterá em um segundo formato XML, mais 
simples, que será interpretado pelo GTeste como estrutura para criação dos roteiros, salvando-os diretamente no banco de dados, sem interferência do usuário.