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


