#!/usr/bin/env python
from argparse import ArgumentParser, Namespace
from functools import cached_property
from typing import List
from urllib.request import urlopen
import json


class CheckGains:
    def __init__(self, values: List[int]) -> None:
        self._repr = "CheckGains: <Value: %s; Rate: %s; Gains: %s;>"
        self.values = values

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
        return sum(self.values) if self.values else 1

    @cached_property
    def gains(self) -> float:
        """
        Returns self.value - 12% multiplied by the exchange rate (dolar)
        rounded to 2
        """
        return round((self.value - (self.value * 0.12)) * self.rate, 2)

    @cached_property
    def display(self) -> str:
        """
        Converts interger representing dolar values to brl minus paypal's
        approximately 12% cut.
        Currency rate source from: https://github.com/fawazahmed0/currency-api
        """
        if not self.values:
            return f"\n$1 =~ R${self.rate:.2f}\n"
        return f"\n${self.value} =~ R${self.gains}\n"

    def __str__(self) -> str:
        return self.display

    def __repr__(self) -> str:
        return self._repr % (self.value, self.rate, self.gains)


def get_args() -> Namespace:

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
        parser.add_argument(*opt.pop("opt"), **opt)  # type: ignore
    args = parser.parse_args()
    return args


def main() -> None:

    try:
        args: Namespace = get_args()
        print(CheckGains(values=args.values))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
