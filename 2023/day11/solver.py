#!/bin/python3.9
import argparse
import logging
import numpy as np

from itertools import combinations

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


def find_empty(universe, axis):
    empty = []
    if axis == 0:
        for i, r in enumerate(universe):
            if np.all(r == "."):
                empty.append(i)
    elif axis == 1:
        for j in range(universe.shape[1] - 1, -1, -1):
            if np.all(universe[:, j] == "."):
                empty.append(j)
    return empty


def calculate_distance(g1, g2, er, ec, expansion, logger):
    x = abs(g1[0] - g2[0])
    y = abs(g1[1] - g2[1])
    logger.debug(f"distance is {x + y}")
    if any([_ in er for _ in range(min(g1[0], g2[0]), max(g1[0], g2[0]))]):
        x += sum([_ in er for _ in range(min(g1[0], g2[0]), max(g1[0], g2[0]))]) * (
            expansion - 1 if expansion > 1 else 1
        )
    if any([_ in ec for _ in range(min(g1[1], g2[1]), max(g1[1], g2[1]))]):
        y += sum([_ in ec for _ in range(min(g1[1], g2[1]), max(g1[1], g2[1]))]) * (
            expansion - 1 if expansion > 1 else 1
        )
    logger.debug(f"distance is {x + y}")
    return x + y


def solver(args, logger):
    if args.test:
        lines = open("test_input.txt", "r").readlines()
    else:
        lines = open("input.txt", "r").readlines()
    result = 0
    logger.debug(f"dimensions of universe before: {len(lines)}x{len(lines[0].strip())}")
    universe = np.array([list(l.strip()) for l in lines])
    logger.debug(f"dimensions of universe after: {universe.shape}")

    galaxyes = [(x, y) for x, y in zip(*np.where(universe == "#"))]
    galaxyes = [(g, i + 1) for i, g in enumerate(galaxyes)]

    empty_rows = find_empty(universe, 0)
    empty_cols = find_empty(universe, 1)
    logger.debug(f"empty rows: {empty_rows}")
    logger.debug(f"empty cols: {empty_cols}")

    if args.part == 1:
        for g1, g2 in combinations(galaxyes, 2):
            logger.debug(f"Comparing {g1[1]} and {g2[1]}")
            distance = calculate_distance(
                g1[0], g2[0], empty_rows, empty_cols, 1, logger
            )
            logger.debug(f"Distance: {distance}")
            result += distance

    elif args.part == 2:
        for g1, g2 in combinations(galaxyes, 2):
            logger.debug(f"Comparing {g1[1]} and {g2[1]}")
            distance = calculate_distance(
                g1[0], g2[0], empty_rows, empty_cols, 1000000, logger
            )
            logger.debug(f"Distance: {distance}")
            result += distance

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2023 - ")
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
