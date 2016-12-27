from twisted.trial import unittest
from invest import Investment

class InvestmentestCase(unittest.TestCase):
    def test_calculateCompoundInterest(self):
        invest = Investment()
        investedValue = invest.calculateCompoundInterest(5)
        self.assertEqual(investedValue, 40.58)
