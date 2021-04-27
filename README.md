# Candlestick of Bitcoin


<!-- Sumário -->
<details open="open">
    <summary>Sumário </summary>
    <ol>
        <li> <a href="#description">Descrição</a></li>
        <li><a href="#details">Detalhes Técnicos</a></li>
        <li> <a href="#phases">Etapas</a></li>
        <li> <a href="#installation">Instalação</a>
            <ul>
                <li><a href="#prerequisites">Pré-requisitos</a></li>
                <li><a href="#usage">Para reproduzir (com docker)</a></li>
                <li><a href="#local-test">Testar localmente (sem docker)</a></li>
            </ul>
        </li>
        </li>
    </ol>
</details>

## Descrição

Aplicação em Flask usando biblioteca bokeh para construir candlesticks de valores do bitcoin extraídos da API Poloniex 


## Detalhes técnicos

- Linguagem utilizada: Python  3.7 / Flask  
- Plataforma/Editor: Visual Studio Code
- Bibliotecas utilizadas: Disponível no arquivo requirements.txt
- Banco de dados: mysql
- Docker
- Fonte de dados: https://docs.poloniex.com/#public-http-api-methods (returnTicker)


## Etapas
1. Criação do arquivo base app.py
2. Instalação de pacotes necessários 
 ```sh
   pip install nome-pacote
   ```
3. Testes no virtualenv em modo de desenvolvimento


## Instalação

  ### Pré-requisitos
  1. Ter docker instalado
  
### Para reproduzir:
1. Clone o repositório
  ```sh
   git clone https://github.com/nayaras/flask-bokeh-poloniex.git
   ```
2. Executar docker-compose na pasta:
 ```sh
   docker-compose up
   ```
3. Abrir página web:
```sh
   localhost:5000
   ```
### Testar localmente:

1. Pré-requisitos:
- Python instalado (pip)
- Mysql server instalado

2. Clone repositório e abra o projeto no seu ambiente de desenvolvimento 
3. Instalar dependencias 
```
pip install requirements.txt
```
5.  Instalar vitualenv
```
pip install virtualenv
```
3. Ativar virtual env

```
venv\Scripts\activate 
```
4. Setar variáveis de desenvovimento
```
set FLASK_ENV=development
set FLASK_APP=app.py
```
5. Rodar script de criação de banco de dados e tabela (usei workbench) [file: init.sql]
6. Rodar projeto:
```
flask run
```
7. Abrir página web:
```sh
   localhost:5000
   ```
