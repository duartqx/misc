#!/usr/bin/env python
import json
import sys
from urllib.request import urlopen


class CheckGains:

    def __init__(self, *args) -> None:
        self.DR = self.check_rate()
        self.to_check = args
        self.gains = self.__gains()

    def check_rate(
        self, url: str='https://cdn.jsdelivr.net/gh/fawazahmed0/currency' \
                       '-api@1/latest/currencies/usd/brl.min.json'
    ) -> float:
        ''' Returns the current rate of dolars in brl '''
        return json.load(urlopen(url)).get('brl')

    def __help(self) -> str:
        return '''
    Usage:
        checkgains
            prints out the dolar exchange rate for today in brl
        checkgains [number|int|float]
            prints out the gains calculated with today's exchange rate
        '''

    def __check_gains(self, L: float,) -> float:
        '''
            Returns L - 7% multiplied by the exchange rate (dolar)
            rounded to 2
        '''
        return round((L - (L * 0.07)) * self.DR, 2)

    def __gains(self) -> str:

        if '--help' in self.to_check:
            return self.__help()

        __gains: str = '\n'

        if len(self.to_check) == 2:

            for index, prefix in enumerate(('Pending', 'Total')):
                L = float(self.to_check[index])
                G: float = self.__check_gains(L)
                __gains += f'{prefix} ${L} -> R${G}\n'

            return __gains
        else:

            for l in self.to_check:
                L = float(l)
                G = self.__check_gains(L)
                __gains += f'${l} -> R${G}\n'

            return __gains

    def __call__(self) -> None:
        ''' Check dolar to brl exchange rate and prints out it minus paypal's
            7% cut
            Currency api provided for free at
            https://github.com/fawazahmed0/currency-api
        '''

        if '--help' in self.to_check:
            print(self.__help())
        elif not self.to_check:
            print(f'R${self.DR:.2f}')
        else:
            try:
                print(self.gains)
            except ValueError:
                print(
                    'Argument must be a number\n',
                    self.__help(),
                    file=sys.stderr
                )
                sys.exit(1)

if __name__ == '__main__':
    
    CheckGains(*sys.argv[1:])()
