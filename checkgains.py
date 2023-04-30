#!/usr/bin/env python
from argparse import ArgumentParser, Namespace
from functools import cached_property
from urllib.request import urlopen
import json


class CheckGains:
    def __init__(self) -> None:
        self._repr = "CheckGains: <Value: %s; Rate: %s; Gains: %s;>"
        self.args = self._get_args()

    def _get_args(self) -> Namespace:

        parser = ArgumentParser(
            prog="CheckGains",
            description="Prints out the dolar exchange rate for today in brl.",
        )
        options = [
            {
                "opt": ("values",),
                "metavar": "values",
                "type": int,
                "nargs": "*",
                "help": "integer accumulator",
            },
        ]
        for opt in options:
            parser.add_argument(*opt.pop("opt"), **opt)
        args = parser.parse_args()
        return args

    @cached_property
    def rate(self) -> float:
        """Returns the current rate of dolars in brl"""
        url: str = (
            "https://cdn.jsdelivr.net/gh/fawazahmed0/currency"
            "-api@1/latest/currencies/usd/brl.min.json"
        )
        return json.load(urlopen(url)).get("brl")

    @cached_property
    def value(self) -> int:
        return sum(self.args.values) if self.args.values else 1

    @cached_property
    def gains(self) -> float:
        """
        Returns self.value - 12% multiplied by the exchange rate (dolar)
        rounded to 2
        """
        return round((self.value - (self.value * 0.12)) * self.rate, 2)

    def __str__(self) -> str:
        """
        Converts interger representing dolar values to brl minus paypal's
        approximately 12% cut.
        Currency rate source from: https://github.com/fawazahmed0/currency-api
        """
        if not self.args.values:
            return f"\n$1 =~ {self.rate:.2f}\n"
        return f"\n${self.value} =~ {self.gains}\n"

    def __repr__(self) -> str:
        return self._repr % (self.value, self.rate, self.gains)


if __name__ == "__main__":

    try:
        print(CheckGains())
    except KeyboardInterrupt:
        pass
