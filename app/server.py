import os
import jinja2
from klein import Klein


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


if __name__ == "__main__":
    app.run('127.0.0.1', 8080)
