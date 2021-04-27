# Candlestick of Bitcoin


<!-- Sumário -->
<details open="open">
    <summary>Sumário </summary>
    <ol>
        <li><a href="#descrição">Descrição</a></li>
        <li><a href="#detalhes-técnicos">Detalhes Técnicos</a></li>
        <li><a href="#etapas">Etapas</a></li>
        <li><a href="#instalação">Instalação</a>
            <ul>
                <li><a href="#pré-requisitos">Pré-requisitos</a></li>
                <li><a href="#para-reproduzir">Para reproduzir</a></li>
                <li><a href="#testar-localmente">Testar localmente</a></li>
            </ul>
        </li>
        <li><a href="#observações">Observações</a>
        <li><a href="#referências">Referências</a>
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
```sh
pip install requirements.txt
```
5.  Instalar vitualenv
```sh
pip install virtualenv
```
3. Ativar virtual env

```sh
venv\Scripts\activate 
```
4. Setar variáveis de desenvovimento
```sh
set FLASK_ENV=development
set FLASK_APP=app.py
```
5. Rodar script de criação de banco de dados e tabela (usei workbench) [file: init.sql]
6. Rodar projeto:
```sh
flask run
```
7. Abrir página web:
```sh
   localhost:5000
   ```
 
 ## Observações
 1. Testei local com uma lib de integração do flask com mysql e quando fui subir pro docker, nenhuma versão do python aceitava a instalação, o que me fez ter que usar o conector do mysql pra python
 2. Não deu tempo de realizar testes unitários até o momento (vou colocar em outro branch, após o prazo)
 3. A única solução para flask que encontrei para recarregar o gráfico do candlestick foi atualizar a página (via jquery), embora tenha testado soluções de renderizar somente a div ou uma parte do template html especifico (sem sucesso) 
 3.1. Como solução futura: trocar framework (talvez django resolva) ou estudar o bokeh server
 4. Testei o plotly para gerar a visualização do candlestick, mas para aplicação web achei o bokeh mais indicado
 5. A tabela presente só possui front (css e html puro) para mostrar a requisição atual, sem armazenamento de dados
 
 ## Referências
 1. Docker: https://docs.docker.com/compose/gettingstarted/
 2. Bokeh: https://docs.bokeh.org/en/latest/docs/gallery/candlestick.html / http://perfspy.blogspot.com/2017/03/candlestick-chart-using-boken-without.html
 3. Conector MySql: https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
 
