#!/bin/python3.9
import re
import argparse
import logging

from collections import namedtuple

from math import inf

logger_local = logging.getLogger("day02")


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


configuration = {
    "red": 12,
    "blue": 14,
    "green": 13,
}

colors = set(["red", "green", "blue"])

Record = namedtuple("record", ["red", "green", "blue"])


def solver(args, logger):
    lines = open("input.txt", "r").readlines()
    games = {int(l.split(":")[0].split()[1]): [] for l in lines}
    result = 0
    for id, game in enumerate(lines):
        extractions = game.split(":")[1].split(";")
        for e in extractions:
            if e.strip() != "":
                r_dict = {v: int(k) for k, v in re.findall(r"(\d+) (\w+)", e)}
                diff = colors - set(r_dict.keys())
                while len(diff) > 0:
                    r_dict[diff.pop()] = 0
                r = Record(**r_dict)
                games[id + 1].append(r)
    if args.part == 1:
        np = []
        p = []
        for id, g in games.items():
            possible = True

            for r in g:
                if (
                    r.red > configuration["red"]
                    or r.green > configuration["green"]
                    or r.blue > configuration["blue"]
                ):
                    possible = False
                    np.append(id)
                    break
            if possible:
                p.append(id)
                result += id

        logger.debug(f"Possible: {p}")
        logger.debug(f"Not Possible: {np}")
        logger.debug(f"Result: {result}")
        logger.debug(f"len(p): {len(p)}")
        logger.debug(f"len(np): {len(np)}")
        logger.debug(f"len : {len(p)+len(np)}")

    else:
        for id, g in games.items():
            minimum_configuration = Record(red=0, green=0, blue=0)
            for r in g:
                if r.red > minimum_configuration.red:
                    minimum_configuration = minimum_configuration._replace(red=r.red)
                if r.green > minimum_configuration.green:
                    minimum_configuration = minimum_configuration._replace(
                        green=r.green
                    )
                if r.blue > minimum_configuration.blue:
                    minimum_configuration = minimum_configuration._replace(blue=r.blue)
            logger.debug(
                f"Game {id}: {minimum_configuration} -> {minimum_configuration.red * minimum_configuration.green * minimum_configuration.blue}"
            )
            result += (
                minimum_configuration.red
                * minimum_configuration.green
                * minimum_configuration.blue
            )

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 2: Cube Conundrum"
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
    logger_local.info(solution)
