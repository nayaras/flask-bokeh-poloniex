from flask import Flask, render_template, request, jsonify
import requests
import json
from datetime import datetime
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    CrosshairTool,
    SingleIntervalTicker,
    LinearAxis,
    DatetimeTickFormatter,
)
import numpy as np

import pandas as pd

from db import select, insert, update

# ativar: venv\Scripts\activate
# set FLASK_ENV=development
# set FLASK_APP=app.py
app = Flask(__name__, static_url_path="")

app.config["TEMPLATES_AUTO_RELOAD"] = True


##funcao para api rest (requisição get na url do poloniex)
def get_data():
    try:
        url = "https://poloniex.com/public?command=returnTicker"

        res = requests.get(url)
        #pega a data da requisição no header 
        date = res.headers["Date"]
        print(date)

        # with open('out.json', 'w') as outfile:
        #     json.dump(res.json(), outfile)

    except:
        print("An exception occurred")

    return res, date


##função de ciação do gráfico candlestick
def create_candlestick(time):
    try:
        rows = select(time)
        print('aqui')
        print("[DEBUG ::] ", len(rows), "linhas obtidas.")

        #transfere dados do bd para dataframe
        df = pd.DataFrame(rows, columns=["data_hora", "open", "low", "high", "close"])
        
        seqs = np.arange(df.shape[0])
        df["seq"] = pd.Series(seqs)
        
        #altera formato da data
        df["data_hora"] = pd.to_datetime(df["data_hora"])
        df["data_hora"] = df["data_hora"].apply(lambda x: x.strftime("%d/%m/%y %H:%M:%S"))

        #reaproveitado de exemplo do próprio bokeh 
        df["mid"] = df.apply(lambda x: (x["open"] + x["close"]) / 2, axis=1)
        df["height"] = df.apply(
            lambda x: abs(x["close"] - x["open"] if x["close"] != x["open"] else 0.001),
            axis=1,
        )

        inc = df.close > df.open
        dec = df.open > df.close
        w = 0.3

        sourceInc = ColumnDataSource(ColumnDataSource.from_df(df.loc[inc]))
        sourceDec = ColumnDataSource(ColumnDataSource.from_df(df.loc[dec]))

        #insere visualização em cima de cada candle
        hover = HoverTool(
            tooltips=[
                ("data/hora", "@data_hora"),
                ("open", "@open{1.1111}"),
                ("close", "@close{1.1111}"),
            ]
        )

        TOOLS = [CrosshairTool(), hover]

        # range do eixo y (pego o maior e menor valor da moeda como base)
        max_value = df["high"].max() + 300
        min_value = df["low"].min() - 300

        p = figure(
            x_axis_label="Horário (UTC)",
            y_axis_label="Valor (US$)",
            plot_width=700,
            plot_height=400,
            tools=TOOLS,
            title="Candlestick - Bitcoin (USDT-BTC) ",
            y_range=(min_value, max_value),
        )

        #formata eixo x para aparecer horario da requisicao dos valores
        p.xaxis.major_label_overrides = {
            i: date.strftime('%H:%M') for i, date in enumerate(pd.to_datetime(df["data_hora"]))
        }
        
        p.grid.grid_line_alpha = 0.3

        # this is the up tail
        p.segment(df.seq[inc], df.high[inc], df.seq[inc], df.low[inc], color="red")

        # this is the bottom tail
        p.segment(df.seq[dec], df.high[dec], df.seq[dec], df.low[dec], color="green")

        # this is the candle body for the red dates
        p.rect(
            x="seq",
            y="mid",
            width=w,
            height="height",
            fill_color="red",
            line_color="red",
            source=sourceInc,
        )

        # this is the candle body for the green dates
        p.rect(
            x="seq",
            y="mid",
            width=w,
            height="height",
            fill_color="green",
            line_color="green",
            source=sourceDec,
        )

        return p

    except:
        print('[DEBUG ::]  Erro ao gerar candlestick. Verificar requisição ao bd')
    
        
#tempo default
tempo = "1"
@app.route("/", methods=["GET", "POST"])
def home():
    global tempo #corrige erro de local variable
    if request.method == "GET":
        #se houver troca do tempo no dropdown, regarrega a page
        if "selected_index" in request.args:
            tempo = request.args.get("selected_index")

    #request poloniex assim que a página é chamada               
    res = get_data()

    if res[0].status_code == 200:
        resposta = res[0].json()
        moedas_selecionadas = [
            "USDT_BTC",
            "USDC_BTC",
            "BTC_BTS",
            "BTC_DASH",
            "BTC_DOGE",
            "BTC_LTC",
        ]
        #print("resp ", resposta["USDT_BTC"]["last"])

        #atualiza close do ultimo candle inserido com valor open do novo candle
        # obs.: solucao temporária pois api não fornece valor close (considerando que last seja o open)
        update(resposta["USDT_BTC"]["last"])

        #insere response da api poloniex no bd
        insert(res[1], resposta, tempo)

        # seta recursos estáticos para visualização do candle
        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()
        candlestick = create_candlestick(tempo)
        script, div = components(candlestick)
      
        #renderiza page html
        return render_template(
            "index.html",
            cotacao=resposta,
            moedas=moedas_selecionadas,
            data_requisicao=res[1],
            periodo=tempo,
            plot_script=script,
            plot_div=div,
            js_resources=js_resources,
            css_resources=css_resources,
        )
        
    else:
        return render_template("index.html")
        
