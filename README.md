# bitrix-users-update
Este projeto realiza a atualização de usuários no CRM Bitrix, sincronizando dados com outras plataformas.

## Funcionalidades
* Atualização de dados de identificação dos funcionário
* Adicição de usuários novos ao grupo de trabalho principal da empresa

## Ferramentas Utilizadas
### Python 3.10
Biblitecas:
  (disponíveis no [requirements.txt](https://github.com/vbs-matheus/bitrix-users-update/blob/main/requirements.txt))
### Bitrix24
O Bitrix24 funciona como origem e destino dos dados a serem atualizados. Por vezes, precisamos fazer comparações 'de-para' entre dados presentes dentro CRM e dados em bases de dados externas.
### Como funciona
Os códigos presentes nesse repositório funcionam a partir da inicialização direta dos programas e precisam apenas do acesso às bases de dado do CRM.
