from mock import Mock, MagicMock, patch

import pytest

import server
import db


@pytest.fixture
def request():
	request = MagicMock()
	return request


def test_home(request):
	""" Do I render the home page? """
	ret = server.home(request)
	assert 'How much money are you about to spend?' in ret


def test_invest(request):
	""" Do I render the invest page? """
	ret = server.invest(request, 2)
	assert '$2 could be worth <strong>$16.23' in ret


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


def test_daily_stock_with_symbol(request):
	""" Do I render the daily stock page? """
	request.args = {'symbol': ['INDEX_GSPC']}
	ret = server.daily_stock(request)
	assert 'Daily Stock Data for' in ret


def test_get_ohlvc(request):
	""" Do I return the recent stock data? """
	pGetRecentOhlvc = patch.object(db, 'get_recent_ohlvc', return_value='stuff')
	with pGetRecentOhlvc:
		ret = server.get_ohlvc(request, 'INDEX_GSPC')
		assert 'stuff' in ret


def test_update_ohlvc(request):
	""" Do I get start date and save the stock data? """
	request.args = {'symbol': ['INDEX_GSPC']}
	pNeedRecentData = patch.object(db, 'need_recent_data', return_value=True)
	pSymbolExists = patch.object(db, 'symbol_exists', return_value=True)
	with patch('db.save_stock_data'), patch('db.get_start_date'), patch('quandl.get'), pNeedRecentData, pSymbolExists:
		ret = server.update_ohlvc(request)
		db.save_stock_data.assert_called_once()
		db.get_start_date.assert_called_once()
		request.redirect.assert_called_once_with('/dailystock/?symbol=INDEX_GSPC')


def test_update_ohlvc_no_symbol(request):
	""" Do I get start date and save the stock data? """
	pSymbolExists = patch.object(db, 'symbol_exists', return_value=False)
	with pSymbolExists:
		ret = server.update_ohlvc(request)
		assert "error" in ret
