import requests
def pr(jyd):
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}
    url = '/spot/tickers?currency_pair='+jyd+''
    r = requests.request('GET', host + prefix + url, headers=headers)
    return r.json()[0]