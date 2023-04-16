#!/usr/env python
from argparse import ArgumentParser, Namespace


def get_parsed_args() -> Namespace:
    parser = ArgumentParser(prog="add5p")
    for option in [
        {
            "dest": "value",
            "help": "Value to be multiplied by percentage",
            "type": int,
        },
        {
            "option_string": ["-p", "--percentage"],
            "help": "Percentage to multiply value with",
            "action": "store",
            "type": int,
        },
    ]:
        if option.get("option_string"):
            parser.add_argument(*option.pop("option_string"), **option)
        else:
            parser.add_argument(**option)

    return parser.parse_args()


def main() -> None:
    args: Namespace = get_parsed_args()
    percentage: float = (args.percentage / 100) if args.percentage else 0.05
    return args.value + (args.value * percentage)


if __name__ == "__main__":
    print(main())