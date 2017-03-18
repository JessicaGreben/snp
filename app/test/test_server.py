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

def test_saveOhlvc(request):
	""" Do I get start date and save the stock data? """
	with patch('db.save_stock_data'), patch('db.get_start_date'), patch('quandl.get'):
		ret = server.saveOhlvc(request)
		db.save_stock_data.assert_called_once()
		db.get_start_date.assert_called_once()
		assert 'ok' in ret