import os
from datetime import timedelta, datetime, date

import quandl
from quandl.errors.quandl_error import NotFoundError
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


def symbol_exists(symbol):
    """ check if the symbol exists in the database """
    with conn.cursor() as cursor:
        cursor.execute("SELECT exists (SELECT 1 FROM ohlcv WHERE symbol = %s LIMIT 1)", (symbol,))
        symbol, = cursor.fetchone()
        return symbol


def get_recent_ohlvc(symbol):
    """ get the last 10 days of data for a stock symbol """
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM ohlcv WHERE symbol = %s ORDER BY date DESC LIMIT 10", (symbol,))
        recent_ohlvc_data = cursor.fetchall()
        lastTenDaysData = []
        for day in recent_ohlvc_data: 
            lastTenDaysData.append([str(value) for value in day])
        # FIXME should transform data here to something like:
        # {'symbol': lastTenDaysData[0], 'open': lastTenDaysData[1]...etc}
        # then update route and view where this is rendered
        return lastTenDaysData


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


def need_recent_data(symbol):
    """ if we have data from today in the db we don't need more recent data"""
    todays_date = datetime.today()
    todays_day = date(todays_date.year, todays_date.month, todays_date.day)
    delta_days =  todays_day - get_start_date(symbol)
    return delta_days != 0


def is_valid_symbol(symbol):
    try:
        quandl.get("YAHOO/{}".format(symbol), row=1)
        return True
    except NotFoundError:
        return False
