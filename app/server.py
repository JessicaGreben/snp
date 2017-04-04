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
def daily_stock(request):
    """ """
    try:
        symbol = request.args.get('symbol')[0]
        data = get_ohlvc(request, symbol)
    except:
        data = ''
    page = app.templates.get_template('dailystock.html')
    return page.render(ohlvc_data=data)

@app.route('/api/v1/getohlvc/')
def get_ohlvc(request, symbol):
    """ return last 10 days of recent daily stock data for a symbol """
    recent_ohlvc_data = db.get_recent_ohlvc(symbol)
    return recent_ohlvc_data

@app.route('/api/v1/saveohlvc/', methods=['POST'])
def update_ohlvc(request):
    """ get and save all recent daily stock data for a symbol """
    symbol = request.args.get('symbol')[0]
    if db.symbol_exists(symbol):
        if db.need_recent_data(symbol):
            start_date = db.get_start_date(symbol)
            ohlvc_data = quandl.get("YAHOO/{}".format(symbol), start_date=start_date)
            db.save_stock_data(ohlvc_data, symbol)
        return request.redirect('/dailystock/?symbol={}'.format(symbol))
    else:
        return {'status':'error', 'error': 'Symbol %s doesnt exist' % symbol}

if __name__ == "__main__":
    quandl.ApiConfig.api_key = os.environ.get('QUANDL_API_KEY')
    os.environ['ENV_MODE'] = 'prod'
    app.run('127.0.0.1', 8080)
