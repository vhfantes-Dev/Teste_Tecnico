# Utilizando o backend em Python

aqui vai um guia para rodar o servidor em python usando o cmd


## Entrando no diretorio backend
Primeiro precisamos entrar na pasta backend com esse comando

```sh
cd backend
```
### Após entrar no diretório backend siga o próximo passo

## Instalando os requisitos
Para baixar os requisitos use o comando:
```sh
pip install -r requeriments.txt
``` 

### ⚠️ ATENÇÃO!
### O PASSO ACIMA É MUITO IMPORTANTE, SEM ELE VAI ACARRETAR A MUITOS ERROS
### CASO NÃO TENHA O PIP, INSTALE  

(o arquivo requeriments.txt já está na pasta backend)


## Rodando o main.py
Para rodar o aquivo principal main.py precisamos utilizar este comando

```sh
py main.py
```
### Não alterar nenhum arquivo pois poderá causar problemas
### Todas a funções que o backend deve fazer estão sendo chamdas na main.py

## Entrando no diretório da API
Para o consumo da api deveremos entrar na pasta chamada API com este comando
```sh
cd api
```
### Após entrar no diretório api siga o próximo passo

## Rodando a API
Estando no diretório api execute este comando
```sh
uvicorn api.app:app --reload
```
### Este comando fará com que o arquivo app.py dentro da pasta api
### começe a rodar o servidor para usar a api
