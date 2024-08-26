import os
import requests

def transform_quantity(quantity, currency):

    url = 'http://data.fixer.io/api/convert?access_key={}&from=RUB&to={}&amount={}'.format(os.getenv('API_KEY'), currency, quantity)
    
    req = requests.get(url=url)
    
    answer = req.json()

    if answer['success']:
        quantity = answer['result']

    return quantity