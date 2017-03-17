import os
from datetime import timedelta

import psycopg2


def connect():
    """ connect to the database """
    if os.environ.get('ENV_MODE') == 'test':
        db = 'testsnp'
    else:
        db = 'snp'

    return psycopg2.connect(database=db,
        user=os.environ.get('DB_USER'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'))

conn = connect()

def get_start_date(symbol):
    """ get the most recent date that we have daily stock data """
    with conn.cursor() as cursor:
        cursor.execute("SELECT MAX(date) FROM ohlcv WHERE symbol = %s", (symbol,))
        start_date, = cursor.fetchone() # returns none if there are no records

    if start_date:
        start_date += timedelta(days=1)

    return start_date


def save_stock_data(data, symbol):
    """ save daily stock data """
    with conn.cursor() as cursor:
        for record in data.itertuples():
            cursor.execute(
                "INSERT INTO ohlcv (symbol, date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (symbol, record[0], record[1], record[2], record[3], record[4], record[5]),
            )
        conn.commit()

def drop_ohlcv_table():
    """ drop ohlcv data but only when using the test database """
    assert os.environ.get('ENV_MODE') == 'test', 'Not using test database, but trying to drop the ohlvc table'
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM ohlcv")
