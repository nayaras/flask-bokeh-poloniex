from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user="root",
        password="123456",
        database="smarttbot"
    ) as connection:

        create_btc_table_query = """
        CREATE TABLE cotacao(
            id INT AUTO_INCREMENT PRIMARY KEY,
            moeda_label VARCHAR(100),
            moeda_cod VARCHAR(100),
            periodicidade VARCHAR(100),
            data_hora DATETIME,
            open DOUBLE,
            low DOUBLE,
            high DOUBLE,
            close DOUBLE
        )
        """
        with connection.cursor() as cursor:
            cursor.execute(create_btc_table_query)
            connection.commit()
        print('Sucess', connection)
except Error as e:
    print(e)

class Cotacao:
    def add_cotacao(moeda_cod, periodicidade, open, low, high, close):
        try:
            cursor = self.myCon.cursor()  
            moeda_label = ''   
            if(moeda_cod == 'BTC')
                moeda_label = 'Bitcoin'
            date_time=datetime.datetime.now()
            print(tdate)
            sql_insert_query="insert into cotacao (moeda_label, moeda_cod, periodicidade, data_hora, open, low, high, close) values ('"+ moeda_label +"','"+ moeda_cod +"','"+ periodicidade +"','"+ date_time +"', '"+ open +"','"+ low +"','"+ high +"','"+ close +"')";  
            
            mycursor.execute(sql_insert_query)
            self.mydb.commit();
            print("Cotação adicionada")
        
        except mysql.connector.Error as error:
            print("Failed to insert query into tbStudent table {}".format(error))
        finally:
            mycursor.close()
