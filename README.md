# Desafio aula de Python

## Sistema bancário versão 3

Nesse desafio foi atualizado o sistema bancário para modelo em POO.

## Obejtivo do desafio

Iniciar a modelagem do sistema bancário em POO. Adicionar classes para Cliente, Conta e as operações bancárias.

Detalhes do desafio :
 - Dados armazenados em objetos ao invés de dicionários.
 - Código segue o modelo de classes UML
 - Atualizar os métodos que tratam as opções do menu, para funcionarem com classes modeladas.

## Funções Extras

Funções que não fazem parte do desafio, mas cuja implementação eu achei necessária.

- Menu inicial para os cadastros de Usuários e Contas.
- Menu Principal onde as transações são feitas.
- Visualização somente do saldo.
- Além do CPF o Nome do usuário também é um requirimento para entrar no menu principal

Essa versão do ponto de vista do usuário funciona igualmente á versão 2 com algumas pequenas mudanças, como o acréscimo de data e hora da transação
no extrato. Endereço agora é um campo único ao invés de vários campos, e o limite de saques é ligado a conta tirando a necessidade de resetar ele quando
o usuário sai do menu principal.

Assim como as versões anteriores, foi adicionado paradas onde o usuário deve pressionar Enter para continuar, assim facilitando a leitura do resultado
da transação e garantindo que o usuário perceba se houve erro ou não.
