from mock import Mock, patch

import pytest

import server
import db
from invest import Investment


def test_home(request):
	""" Do I render the home page? """
	ret = server.home(request)
	assert 'How much money are you about to spend?' in ret


def test_invest(request):
	""" Do I render the invest page? """
	with patch.object(Investment, 'get_compound_interest', return_value={'rate': 'poo', 'return_value': 'more poo'}):
		ret = server.invest(request, 2)
	assert '$2 could be worth <strong>$more poo' in ret


def test_initInvestSubmit(request):
	""" Do I calculate the initial investment?  """
	with patch('server.invest'):
		server.initInvestSubmit(request)
		server.invest.assert_called_once_with(request,1)


def test_learnToInvest(request):
	""" Do I render the resource page?"""
	ret = server.learnToInvest(request)
	assert 'Learn more about investing' in ret


def test_daily_stock(request):
	""" Do I render the daily stock page? """
	ret = server.daily_stock(request)
	assert 'Provide a stock symbol' in ret
	assert 'Daily Stock Data for' not in ret


def test_daily_stock_with_symbol(request, seed_test_db):
	""" Do I render the daily stock page? """
	request.args = {'symbol': ['INDEX_GSPC']}
	ret = server.daily_stock(request)
	assert 'Last Ten Days of Stock' in ret


def test_get_recent_ohlvc(request):
	""" Do I return the recent stock data? """
	mock_get_recent_ohlvc = patch.object(db, 'get_recent_ohlvc', return_value='stuff')
	with mock_get_recent_ohlvc:
		ret = server.get_recent_ohlvc(request, 'INDEX_GSPC')
		assert 'stuff' in ret


def test_update_ohlvc(request):
	""" Do I get start date and save the stock data? """
	request.args = {'symbol': ['INDEX_GSPC']}
	mock_need_recent_data = patch.object(db, 'need_recent_data', return_value=True)
	mock_symbol_valid = patch.object(db, 'is_valid_symbol', return_value=True)
	with patch('db.save_stock_data'), patch('db.get_recent_data_date'), patch('quandl.get'), mock_need_recent_data, mock_symbol_valid:
		ret = server.update_ohlvc(request)
		db.get_recent_data_date.assert_called_once()
		db.save_stock_data.assert_called_once()
		request.redirect.assert_called_once_with('/dailystock/?symbol=INDEX_GSPC&error=')


def test_update_ohlvc_not_valid_symbol(request):
	""" Do I get start date and save the stock data? """
	mock_symbol_valid = patch.object(db, 'is_valid_symbol', return_value=False)
	with mock_symbol_valid:
		request.args = {'symbol': ['INDEX_GSPC']}
		ret = server.update_ohlvc(request)
		request.redirect.assert_called_once_with("/dailystock/?symbol=INDEX_GSPC&error={'error': 'symbol does not exist'}")
