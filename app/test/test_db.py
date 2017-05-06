import datetime
from mock import patch

import db


SYMBOL = 'INDEX_GSPC'


def test_get_recent_data_date_no_existing_data(drop_ohlcv_table):
	""" Do I return none as a start date when there is no existing data?  """
	assert db.get_recent_data_date(SYMBOL) == None


def test_get_recent_data_date_with_existing_data(seed_test_db):
	""" Do I return the most recent date start date?  """
        assert db.get_recent_data_date(SYMBOL) == datetime.date(2017, 2, 1)


def test_need_recent_data(seed_test_db):
	""" Do I check if we already have recent data in the database? """
	need = db.need_recent_data(SYMBOL)
	assert True == need
        with patch.object(db, 'get_recent_data_date', return_value=None):
            need = db.need_recent_data('poop')
            assert True == need
