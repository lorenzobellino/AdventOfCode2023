#!/bin/python3.9
import argparse
import logging


from functools import cache

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


@cache
def calculate_arrangement(s, p):
    if not s:
        return len(p) == 0

    if not p:
        return "#" not in s

    result = 0
    if s[0] in ".?":
        result += calculate_arrangement(s[1:], p)

    if (
        s[0] in "#?"
        and p[0] <= len(s)
        and "." not in s[: p[0]]
        and (p[0] == len(s) or s[p[0]] != "#")
    ):
        result += calculate_arrangement(s[p[0] + 1 :], p[1:])

    return result


def solver(args, logger):
    if args.test:
        lines = open("test_input.txt", "r").readlines()
    else:
        lines = open("input.txt", "r").readlines()

    result = 0

    if args.part == 1:
        # r = 0
        springs = [
            (
                l.strip().split(" ")[0],
                tuple(int(n) for n in l.strip().split(" ")[1].split(",")),
            )
            for l in lines
        ]
        for s in springs:
            r = calculate_arrangement(s[0], s[1])
            result += r
            logger.debug(f"Result: {r}")

    elif args.part == 2:
        springs = [
            (
                "?".join([l.strip().split(" ")[0] for i in range(5)]),
                tuple(int(n) for n in l.strip().split(" ")[1].split(",")) * 5,
            )
            for l in lines
        ]
        for s in springs:
            result += calculate_arrangement(s[0], s[1])

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 12: Hot Springs "
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
        "-v", "--verbose", action="store_true", help="Enable debug mode"
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
