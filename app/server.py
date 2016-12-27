import os
import jinja2
from klein import Klein

app = Klein()
app.templates = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

@app.route('/')
def home(request):
    """ get home page """
    page = app.templates.get_template('index.html')
    return page.render()

@app.route('/invest')
def invest(request, init):
    """ how much is the initial investment worth after investing """
    from invest import Investment
    investment = Investment()
    accum = investment.calculateCompoundInterest(init)
    page = app.templates.get_template('invest.html')
    return page.render(initInvest=init, accumulatedInvest=accum)

@app.route('/initInvest/submit', methods=['POST'])
def initInvestSubmit(request):
    """ get initial investment value from form """
    initInvest = int(request.args.get('initInvest')[0])
    return invest(request, initInvest)

if __name__ == "__main__":
    # `Klein.run(host, port)` is doing this:
    # 1. Runs a minimal twisted.web server 
    # 2. Runs the default twisted reactor
    # where port is the TCP port to accept HTTP requests
    # and the host is used to bind the listening socket
    # endpoint_description = "tcp:port=port:interface=host"
    # endpoint = endpoints.serverFromString(reactor, endpoint_description)
    # endpoint.listen(Site(self.resource()))
    # reactor.run()
    app.run('localhost', 8080)
