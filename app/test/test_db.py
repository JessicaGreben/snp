import os
from datetime import date

import psycopg2
import quandl
import pytest

import db


SYMBOL = 'INDEX_GSPC'

@pytest.fixture
def drop_ohlcv_table():
	drop_ohlcv_table = db.drop_ohlcv_table()
	return drop_ohlcv_table


@pytest.fixture
def seed_test_db():
	db.drop_ohlcv_table()
	quandl.ApiConfig.api_key = os.environ.get('QUANDL_API_KEY')
	test_ohlvc_data = quandl.get("YAHOO/{}".format(SYMBOL), start_date='2017-01-01', end_date='2017-02-01')
	seed_test_db =  db.save_stock_data(test_ohlvc_data, SYMBOL)
	return seed_test_db


def test_symbol_exists(seed_test_db):
	""" Do I check for if a symbol is in the database? """
	symbol = db.symbol_exists(SYMBOL)
	assert True == symbol
	no_symbol = db.symbol_exists('boo')
	assert False == no_symbol


def test_get_start_date_no_existing_data(drop_ohlcv_table):
	""" Do I return none as a start date when there is no existing data?  """
	assert db.get_start_date(SYMBOL) == None


def test_get_start_date_with_existing_data(seed_test_db):
	""" Do I return the most recent date start date?  """
	test_ohlvc_data = quandl.get("YAHOO/{}".format(SYMBOL), start_date='2017-01-01', end_date='2017-02-01')
	db.save_stock_data(test_ohlvc_data, SYMBOL)
	assert db.get_start_date(SYMBOL) == date(2017, 2, 2)


def test_need_recent_data(seed_test_db):
	""" Do I check if we already have recent data in the database? """
	need = db.need_recent_data(SYMBOL)
	assert True == need
