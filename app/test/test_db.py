from datetime import timedelta, date
from mock import patch

import db


SYMBOL = 'INDEX_GSPC'


def test_get_recent_data_date_no_existing_data(drop_ohlcv_table):
	""" Do I return none as a start date when there is no existing data?  """
	assert db.get_recent_data_date(SYMBOL) == None


def test_get_recent_data_date_with_existing_data(seed_test_db):
	""" Do I return the most recent date start date?  """
        assert db.get_recent_data_date(SYMBOL) == date(2017, 2, 2)


def test_need_recent_data(seed_test_db):
	""" Do I check if we already have recent data in the database? """
	need = db.need_recent_data(SYMBOL)
	assert True == need
        with patch.object(db, 'get_recent_data_date', return_value=None):
            need = db.need_recent_data('poop')
            assert True == need

def test_get_price(seed_test_db):
    """ Do I get the correct price of stock data for the date? """
    today = date(2017,01,31) # tuesday
    price = db.get_price(today, SYMBOL)
    assert price == 2278.870117

    today = date(2017,01,29) # sunday
    price = db.get_price(today, SYMBOL)
    assert price == 2294.6899410000001    