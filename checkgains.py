#!/usr/bin/env python
import json
import sys
from urllib.request import urlopen


def __help() -> str:
    return '''
Usage:
    checkgains
        prints out the dolar exchange rate for today in brl
    checkgains [number|int|float]
        prints out the gains calculated with today's exchange rate 
    '''

def check_rate(url: str) -> float:
    ''' Returns the current rate of dolars in brl '''
    return json.load(urlopen(url)).get('brl')

def check_gains(L: float, DR: float) -> float:
    '''
        Returns L - 7% multiplied by the exchange rate (dolar) rounded to 2
    '''
    return round((L - (L * 0.07)) * DR, 2)

def gains(DR: float, *args) -> str:

    __gains: str = ''

    if len(args) == 2:

        for index, prefix in enumerate(('Pending', 'Total')):
            L = float(args[index])
            G: float = check_gains(L, DR)
            __gains += f'{prefix} ${L} -> R${G}\n'

        return __gains
    else:

        for arg in args:
            L = float(arg)
            G = check_gains(L, DR)
            __gains += f'${arg} -> R${G}\n'

        return __gains

def main() -> None:
    ''' Check dolar to brl exchange rate and prints out it minus paypal's
        7% cut
        Currency api provided for free at
        https://github.com/fawazahmed0/currency-api
    '''
    CURRENCY_API_URL: str = 'https://cdn.jsdelivr.net/gh/fawazahmed0/' \
                            'currency-api@1/latest/currencies/usd/brl.min.json' 

    DOLAR_RATE: float = check_rate(CURRENCY_API_URL)

    args = sys.argv[1:]
    if '--help' in args:
        print(__help())
    if not args:
        print(f'R${DOLAR_RATE:.2f}')
    else:
        try:
            print(gains(DOLAR_RATE, *args))
        except ValueError:
            print(
                'Argument must be a number\n',
                __help(),
                file=sys.stderr
            )
            sys.exit(1)

if __name__ == '__main__':
    
    main()
