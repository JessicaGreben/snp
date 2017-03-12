import pytest

from mock import Mock

from invest import Investment


@pytest.fixture
def investment():
	return Investment()

def test_calculateCompoundInterest(investment):
    investedValue = investment.calculateCompoundInterest(5)
    assert 40.58 == investedValue

