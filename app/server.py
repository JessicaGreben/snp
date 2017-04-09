import os

import jinja2
import quandl
from klein import Klein

import db


app = Klein()
app.templates = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))


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


@app.route('/dailystock/')
def daily_stock(request, data=''):
    """ render the dailystock data page """
    symbol = request.args.get('symbol', [''])[0]
    error = request.args.get('error', [''])[0]
    if symbol and not error:
        data = get_recent_ohlvc(request, symbol)
    page = app.templates.get_template('dailystock.html')
    return page.render(ohlvc_data=data, symbol_error=error, symbol=symbol)


@app.route('/api/v1/getohlvc/')
def get_recent_ohlvc(request, symbol):
    """ return last 10 days of recent daily stock data for a symbol """
    recent_ohlvc_data = db.get_recent_ohlvc(symbol)
    return recent_ohlvc_data


@app.route('/api/v1/saveohlvc/', methods=['POST'])
def update_ohlvc(request, error=''):
    """ get and save all recent daily stock data for a symbol """
    symbol = request.args.get('symbol')[0]
    if db.is_valid_symbol(symbol):
        if db.need_recent_data(symbol):
            start_date = db.get_start_date(symbol)
            ohlvc_data = quandl.get("YAHOO/{}".format(symbol), start_date=start_date)
            db.save_stock_data(ohlvc_data, symbol)
    else:
        error = {'error': 'symbol does not exist'}
    return request.redirect('/dailystock/?symbol={}&error={}'.format(symbol, error))


if __name__ == "__main__":
    quandl.ApiConfig.api_key = os.environ.get('QUANDL_API_KEY')
    os.environ['ENV_MODE'] = 'prod'
    app.run('127.0.0.1', 8080)
