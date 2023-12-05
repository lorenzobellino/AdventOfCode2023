#!/bin/python3.9
import re
import argparse
import logging

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


mapping = {
    "one": "o1e",
    "two": "t2o",
    "three": "thr3e",
    "four": "f4ur",
    "five": "fi5e",
    "six": "s6x",
    "seven": "s7ven",
    "eight": "e8ght",
    "nine": "n9ne",
}


def solver(args, logger):
    lines = open("puzzle.txt", "r").readlines()
    if args.part == 2:
        for m in mapping:
            lines = [l.replace(m, mapping[m]) for l in lines]

    matches = [re.findall(r"\d", line) for line in lines]
    matches = [int(m[0]) * 10 + int(m[-1]) for m in matches]

    logger.debug(f"solution: {sum(matches)}")

    return sum(matches)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 1: Trebuchet?!"
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
        "-v",
        "--verbose",
        help="enable debug logging",
        action="store_true",
        default=False,
    )

    args = parser.parse_args()
    logger_local.setLevel(level=logging.DEBUG if args.verbose else logging.INFO)

    ch = logging.StreamHandler()
    ch.setFormatter(CustomFormatter())

    logger_local.addHandler(ch)
    solution = solver(args, logger_local)
    logger_local.info(f"Solution: {solution}")
