from flask import Flask, render_template, request
import requests
import json
from datetime import datetime
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.models import ColumnDataSource, HoverTool, CrosshairTool, SingleIntervalTicker, LinearAxis, DatetimeTickFormatter
import numpy as np
from flask_mysqldb import MySQL
from flask_apscheduler import APScheduler
import pandas as pd


#ativar: venv\Scripts\activate
#set FLASK_ENV=development
#set FLASK_APP=app.py
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'smarttbot'

mysql = MySQL(app)


def get_data():
    try:
        url = "https://poloniex.com/public?command=returnTicker"

        res = requests.get(url)
        date = res.headers['Date']
        print(date)
        
        resposta = res.json()
        # with open('out.json', 'w') as outfile:
        #     json.dump(res.json(), outfile)
        print('aqui: ', res.json()['USDT_BTC'])
    
    except:
        print("An exception occurred")

    return res, date

def insert(date, resposta):
    last_id_insert = -1
    try:
        cur = mysql.connection.cursor()
        data_hora = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")
        
        cur.execute("INSERT INTO cotacao(moeda_label, moeda_cod, periodicidade, data_hora, open, low, high, close) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    ('Bitcoin', 'USDT_BTC', '1', data_hora, resposta['USDT_BTC']['last'], resposta['USDT_BTC']['lowestAsk'], resposta['USDT_BTC']['highestBid'], resposta['USDT_BTC']['last']))
        mysql.connection.commit()


        #pega o id da última insercao
        last_id_insert = cur.lastrowid
        print('last', last_id_insert)

        cur.close()
    except:
        print('[DEBUG :: DB] Erro ao salvar ultima transacao no BD.')
    
    return last_id_insert
    
def update(close):
    print('chamou pdate')
    try:
        cur = mysql.connection.cursor()
        #pega o id do ultimo candle inserido
        cur.execute("select id from smarttbot.cotacao ORDER BY id DESC LIMIT 1")
        id = cur.fetchone()
        print('id ',id)
        cur.execute("update smarttbot.cotacao set `close` = %s where id =%s",(close,id))
    except:
        print('[DEBUG :: DB] Erro no update do candlestick.')

    
def select(time):
    rows = []
    try:
        cur = mysql.connection.cursor()
        
        cur.execute("select data_hora, open, low, high, close from cotacao where periodicidade= %s", (time))
        rows = cur.fetchall()
        
        cur.close()
        
    except:
        print('[DEBUG :: DB] Erro no select do candlestick.')
    
    return rows


def create_candlestick():
    
    rows = select("1")
    if len(rows) > 0:
        print('[DEBUG ::] ', len(rows), 'linhas obtidas.')
        # for i in rows:
        #     print('teste ',i[0])

    df = pd.DataFrame(rows, columns=['data_hora', 'open', 'low','high','close'])
    print('cols1', df.columns)
    seqs = np.arange(df.shape[0])
    df["seq"] = pd.Series(seqs)
    print(type(df["open"][0]))

    df["data_hora"] = pd.to_datetime(df["data_hora"])
    df['data_hora'] = df['data_hora'].apply(lambda x: x.strftime('%d/%m/%y %H:%M:%S'))
    #df['changepercent']=df['changepercent'].apply(lambda x: str(x)+"%")

    df['mid'] = df.apply(lambda x: (x['open']+x['close'])/2, axis=1)
    df['height'] = df.apply(lambda x: abs(
        x['close']-x['open'] if x['close'] != x['open'] else 0.001), axis=1)

    inc = df.close > df.open
    dec = df.open > df.close
    w = 0.3

    # use ColumnDataSource to pass in data for tooltips
    sourceInc = ColumnDataSource(ColumnDataSource.from_df(df.loc[inc]))
    sourceDec = ColumnDataSource(ColumnDataSource.from_df(df.loc[dec]))

    # the values for the tooltip come from ColumnDataSource
    hover = HoverTool(
        tooltips=[
            ("data/hora", "@data_hora"),
            ("open", "@open{1.1111}"),
            ("close", "@close{1.1111}"),
        ]
    )

    TOOLS = [CrosshairTool(), hover]
    #para setar range do eixo y
    max_value = df["high"].max() + 300
    min_value = df["low"].min() - 300
    p = figure(plot_width=700, plot_height=400, tools=TOOLS,
            title="Candlestick do dia "+df["data_hora"][0], y_range=(min_value, max_value))
    #p.xaxis.major_label_orientation = 50000/4
    p.xaxis.formatter = DatetimeTickFormatter(minutes = ['%M'])


    p.grid.grid_line_alpha = 0.3

    # this is the up tail
    p.segment(df.seq[inc], df.high[inc], df.seq[inc], df.low[inc], color="red")
    # this is the bottom tail
    p.segment(df.seq[dec], df.high[dec], df.seq[dec],
            df.low[dec], color="green")
    # this is the candle body for the red dates
    p.rect(x='seq', y='mid', width=w, height='height',
        fill_color="red", line_color="red", source=sourceInc)
    # this is the candle body for the green dates
    p.rect(x='seq', y='mid', width=w, height='height',
        fill_color="green", line_color="green", source=sourceDec)
    
    return p


@app.route("/get-selected")
def get_selected():
    select = request.form.get('time')
    return redirect(url_for('/'))

@app.route("/", methods=['GET', 'POST'])
def home():
    print('chamou home ',str(datetime.now()))
    res = get_data()
    
    if res[0].status_code == 200:
        resposta = res[0].json()
        moedas_selecionadas = ['USDT_BTC', 'USDC_BTC',
                               'BTC_BTS', 'BTC_DASH', 'BTC_DOGE', 'BTC_LTC']
        print('resp ', resposta['BTC_BTS'])
        update(resposta['USDT_BTC']['last'])

        
        
        
        
        insert(res[1], resposta)
        
        # scheduler = APScheduler()
        # scheduler.add_job(func=get_data, args=[], trigger='interval', id='job', seconds=30)
        # scheduler.start()

        
        # grab the static resources
        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()
        candlestick = create_candlestick()
        script, div = components(candlestick)


        return render_template("index.html", cotacao=resposta, moedas=moedas_selecionadas, data_requisicao=res[1], plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources)
    else:
        return render_template("index.html", cotacao="ERROR")
