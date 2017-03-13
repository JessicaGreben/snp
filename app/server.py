import os
import jinja2
import quandl
import psycopg2
from klein import Klein


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

@app.route('/api/v1/saveohlvc', methods=['POST'])
def saveOhlvc(request):
    """ get and save all recent daily stock data for a symbol """
    import db

    symbol = request.args.get('symbol')[0]
    start_date = db.get_start_date(connection, symbol)
    data = quandl.get("YAHOO/{}".format(symbol), start_date=start_date)
    db.save_stock_data(data, connection, symbol)
    return


if __name__ == "__main__":
    quandl.ApiConfig.api_key = os.environ.get('QUANDL_API_KEY')
    app.run('127.0.0.1', 8080)
