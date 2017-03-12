from mock import Mock, MagicMock, patch

import pytest

import server


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