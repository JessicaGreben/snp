import os
import jinja2
from klein import Klein
import os
import quandl
import psycopg2
from datetime import timedelta

app = Klein()
app.templates = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
connection = psycopg2.connect(database='snp', user='Jessica', host='localhost')


@app.route('/')
def home(request):
    """ render home page """
    page = app.templates.get_template('index.html')
    return page.render()

@app.route('/invest/')
def invest(request, init):
    """ how much is the initial investment worth after investing """
    from invest import Investment

    investment = Investment()
    accum = investment.calculateCompoundInterest(init)
    page = app.templates.get_template('invest.html')
    return page.render(initInvest=init, accumulatedInvest=accum)

@app.route('/initInvest/submit/', methods=['POST'])
def initInvestSubmit(request):
    """ get initial investment value from form """
    initInvest = int(request.args.get('initInvest')[0])
    return invest(request, initInvest)

@app.route('/resources/')
def learnToInvest(request):
    """ render resource page """
    page = app.templates.get_template('resources.html')
    return page.render()

@app.route('/api/v1/getohlvc', methods=['POST'])
def getOhlvc(request):
    """ get all recent daily stock data """
    # when do we do this? on page load? missing method to send the symbol
    # should just return stock data
    symbol = request.args.get('symbol')[0]
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT MAX(date) FROM ohlcv WHERE symbol = %s", (symbol,))
        start_date, = cursor.fetchone() # returns none if there are no records

        if start_date:
            start_date += timedelta(days=1)

        data = quandl.get("YAHOO/{}".format(symbol), start_date=start_date)

        for record in data.itertuples():
            cursor.execute(
                "INSERT INTO ohlcv (symbol, date, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (symbol, record[0], record[1], record[2], record[3], record[4], record[5]),
            )
        connection.commit()
    finally:
        cursor.close()


if __name__ == "__main__":
    quandl.ApiConfig.api_key = os.environ.get('QUANDL_API_KEY')
    app.run('127.0.0.1', 8080)
