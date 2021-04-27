from datetime import datetime
import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'nayara',
  'password': '123456',
  #'host': 'host.docker.internal',
  #'port':'32000',
  'host': 'localhost',
  'port':'3306',
  'database': 'smarttbot',
  'raise_on_warnings': True
}


conn = mysql.connector.connect(**config)
cursor = conn.cursor()

def insert(date, resposta, tempo):
    last_id_insert = -1
    try:
        data_hora = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %Z")

        cursor.execute(
            "INSERT INTO cotacao(moeda_label, moeda_cod, periodicidade, data_hora, open, low, high, close) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                "Bitcoin",
                "USDT_BTC",
                tempo,
                data_hora,
                resposta["USDT_BTC"]["last"],
                resposta["USDT_BTC"]["lowestAsk"],
                resposta["USDT_BTC"]["highestBid"],
                resposta["USDT_BTC"]["last"],
            ),
        )
        conn.commit()

        #cursor.close()
    except mysql.connector.Error as err:
        print("[DEBUG :: DB] Erro ao salvar ultima transacao no BD.", err)

    #return last_id_insert


def update(close):
    try:
        # pega o id do ultimo candle inserido
        cursor.execute("select id from cotacao ORDER BY id DESC LIMIT 1")
        id = cursor.fetchone()
        #print("id ", id[0],type(id[0]), type(close))
        if id != None:
            print('foi')
            cursor.execute(
                "UPDATE cotacao SET close=%s WHERE id=%s", (close, id[0])
            )
            conn.commit()
        
    except mysql.connector.Error as err:
        print("[DEBUG :: DB] Erro no update do candlestick. ", err)


def select(time):
    rows = []
    try:
        # seleciona todo mundo gerado com data maior ou igual data atual
        cursor.execute(
            "SELECT data_hora, open, low, high, close FROM cotacao WHERE data_hora >= CURDATE() ORDER BY data_hora"
        )
        rows = cursor.fetchall()

    except mysql.connector.Error as err:
        print("[DEBUG :: DB] Erro no select do candlestick.", err)

    return rows

