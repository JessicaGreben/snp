import os
import datetime
from mock import MagicMock

import quandl
import pytest

import db
from invest import Investment


SYMBOL = 'INDEX_GSPC'


@pytest.fixture
def investment():
    return Investment()


@pytest.fixture
def request():
    request = MagicMock()
    return request


@pytest.fixture
def engine():
    engine = db.connect()
    return engine


@pytest.fixture
def drop_ohlcv_table(engine):
    drop_ohlcv_table = db.drop_ohlcv_table(engine)
    return drop_ohlcv_table


@pytest.fixture
def seed_test_db(engine):
    quandl.ApiConfig.api_key = os.environ.get('QUANDL_API_KEY')
    test_ohlvc_data = quandl.get("YAHOO/{}".format(SYMBOL), start_date='2017-01-27', end_date='2017-02-02')
    seed_test_db =  db.save_stock_data(test_ohlvc_data, SYMBOL)
    return seed_test_db
