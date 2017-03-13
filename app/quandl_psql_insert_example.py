import os
import quandl
import psycopg2
from datetime import timedelta


SYMBOL = 'INDEX_GSPC'
quandl.ApiConfig.api_key = os.environ.get('QUANDL_API_KEY')

connection = psycopg2.connect(database='snp', user='ryan', host='localhost')

cursor = connection.cursor()


try:
    cursor.execute("SELECT MAX(date) FROM ohlcv WHERE symbol = %s", (SYMBOL,))
    start_date, = cursor.fetchone() # returns none if there are no records

    if start_date:
        start_date += timedelta(days=1)

    data = quandl.get("YAHOO/{}".format(SYMBOL), start_date=start_date)

    for record in data.itertuples():
        cursor.execute(
            "INSERT INTO ohlcv (symbol, date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (SYMBOL, record[0], record[1], record[2], record[3], record[4], record[5]),
        )
    connection.commit()
finally:
    cursor.close()
    connection.close()

