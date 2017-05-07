from mock import Mock, patch
from datetime import date
from dateutil.relativedelta import relativedelta

from invest import Investment
import db


SYMBOL = 'INDEX_GSPC'


def test_get_compound_interest(investment):
    """ Do I calculate compound interest correctly? """
    investedValue = investment.get_compound_interest(5)
    assert {'rate': '7.0%', 'return_value': 38.06} == investedValue


def test_get_compound_interest_with_symbol(investment):
    """ Do I calculate compound interest with the rate for the specific stock?"""
    with patch.object(investment, 'get_annual_return_rate') as p_annual_rate:
        investedValue = investment.get_compound_interest(5, symbol=SYMBOL)
        p_annual_rate.assert_called_once_with(30, SYMBOL)


def test_annual_retrun_rate(investment):
    """ Do I return the annual growth rate for a stock? """
    with patch.object(investment, 'get_simple_return', return_value=9876):
        rate = investment.get_annual_return_rate(30, SYMBOL)
        assert rate == 0.35879571443215186


def test_get_simple_return(investment):
    """ Do I return the simple rate? """
    with patch.object(db, 'get_price', side_effect=[10,5]):
        rate = investment.get_simple_return(30, SYMBOL)
        assert rate == 1.0
