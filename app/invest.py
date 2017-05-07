from __future__ import division
import math
from datetime import date
from dateutil.relativedelta import relativedelta

import db


class Investment(object):
    """
    All the things you can do with your money instead 
    of spending it.
    """
    def get_compound_interest(self, initInvest, years=30, symbol=None):
        """
        What is the potential worth of an amount when subjected
            to compound interest over some amount of time?
        """
        principal = initInvest
        frequency = 1 # compounded annually
        years = years
        rate = self.get_annual_return_rate(years, symbol) if symbol else 0.07
        total = principal * (1+rate/frequency) ** (frequency*years)
        return {'return_value': round(total, 2), 'rate': "{0:.03}%".format(rate * 100)}

    def get_annual_return_rate(self, years, symbol):
        """
        What is the annual growth rate for a specific stock
            over one year?
        """
        simple_return = self.get_simple_return(years, symbol)
        annual_growth_rate = (simple_return +1) ** (1/years) - 1
        return annual_growth_rate

    def get_simple_return(self, years, symbol):
        """
        What is the growth rate for a specific stock over
            an amount of time?
        """
        today = date.today()
        purchase_date = today - relativedelta(years=years)
        current_price = db.get_price(today, symbol)
        purchase_price= db.get_price(purchase_date, symbol)
        annual_rate =  (current_price - purchase_price) / purchase_price
        return annual_rate
