#!/bin/python3.9
import argparse
import logging
import re
from itertools import accumulate
from math import gcd


logger_local = logging.getLogger("day01")


class CustomFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.DEBUG:
            return f"[{record.name}] :: D - {record.msg}"
        elif record.levelno == logging.INFO:
            return f"[{record.name}] :: I - {record.msg}"
        elif record.levelno == logging.WARNING:
            return f"[{record.name}] :: W - {record.msg}"
        elif record.levelno == logging.ERROR:
            return f"[{record.name}] :: E - {record.msg}"
        else:
            return super().format(record)


def solver(args, logger):
    if args.test:
        lines = open("test_input.txt", "r").readlines()
    else:
        lines = open("input.txt", "r").readlines()

    sequences = [re.findall(r"[-]?\d+", l.strip()) for l in lines]
    sequences = [[int(i) for i in s] for s in sequences]

    result = []

    if args.part == 1:
        for s in sequences:
            res = s[-1]
            logger.debug(s)
            while any(s):
                s = [s[i + 1] - s[i] for i in range(len(s) - 1)]
                res += s[-1]
            result.append(res)

    elif args.part == 2:
        for s in sequences:
            res = [s[0]]
            logger.debug(s)
            while any(s):
                s = [s[i + 1] - s[i] for i in range(len(s) - 1)]
                res.append(s[0])
                logger.debug(s)
            result.append(list(accumulate(res[::-1], lambda x, y: y - x))[-1])

    return sum(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 9: Mirage Maintenance"
    )
    parser.add_argument(
        "-p",
        "--part",
        help="part of the challenge to solve (1 or 2)",
        type=int,
        choices=[1, 2],
        required=True,
    )
    parser.add_argument(
        "-t",
        "--test",
        help="test mode",
        action="store_true",
    )
    args = parser.parse_args()
    logger_local.setLevel(level=logging.DEBUG if args.verbose else logging.INFO)

    ch = logging.StreamHandler()
    ch.setFormatter(CustomFormatter())

    logger_local.addHandler(ch)
    solution = solver(args, logger_local)
    logger_local.info(solution)
