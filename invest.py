class Investment:
    """
    All the things you can do with your money instead 
    of spending it
    """

    def calculateCompoundInterest(self, initInvest):
        """
        What is the potential worth of an amount
        when subjected to compound interest
        """
        principal = initInvest
        frequency = 12
        years = 30
        rate = 0.07
        total = principal * (1+rate/frequency) ** (frequency*years) 
        return round(total, 2)
