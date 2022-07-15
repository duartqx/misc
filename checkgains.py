#!/usr/bin/env python
import json
from sys import argv, exit as sysexit
from urllib.request import urlopen
#from re import search, sub

# Currency api provided for free at https://github.com/fawazahmed0/currency-api
CURRENCY_API_URL: str = 'https://cdn.jsdelivr.net/gh/fawazahmed0/' \
                        'currency-api@1/latest/currencies/usd/brl.min.json' 

#def check_rate() -> float:
#    ''' Grabs dolarhoje.com frontpage and scrapes the dolar to brl exchange
#    rate for today '''
#    request: str = urlopen('https://dolarhoje.com').read().decode()
#    dolar_string: str = search(r'\$ (\d+\W\d+)', request).group(1)
#    return float(sub(',', '.', dolar_string))

def check_rate() -> float:
    ''' Returns the current rate of dolars in brl '''
    return json.load(urlopen(CURRENCY_API_URL))['brl']

def check_gains(L: float, dolar: float) -> float:
    ''' Returns L - 7% multiplied by the exchange rate (dolar) rounded to 2 '''
    return round((L - (L * 0.07)) * dolar, 2)

def main() -> None:
    ''' Check dolar to brl exchange rate and prints out it minus paypal's 7%
    cut '''
    dolar: float = check_rate()
    try:
        arg_1 = argv[1]
        if arg_1 == '--check': print(f'R${dolar:.2f}')
        else:
            try:
                L = float(arg_1)
                gains: float = check_gains(L, dolar)
                print(f'R${gains}')
            except ValueError:
                print('Argument must be a number')
                sysexit(1)
    except IndexError:
        print('''Usage:
            checkgains --check
                prints out the dolar exchange rate for today in brl
            checkgains [number|int|float]
                prints out the gains calculated with today's exchange rate ''')

if __name__ == '__main__':
    
    main()
