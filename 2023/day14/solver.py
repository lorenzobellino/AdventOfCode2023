#!/bin/python3.9
import argparse
import logging

import numpy as np

from itertools import cycle

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


def calculate_load(platform, logger):
    load = 0
    for r in range(len(platform)):
        round_rock = np.count_nonzero(platform[r, :] == "O")
        load += round_rock * (len(platform) - r)
    return load


def tilt(platform, direction, logger):
    if direction == "N":
        for c in range(len(platform[0])):
            # logger.debug("Tilting North")
            rocks = np.where(platform[:, c] == "#")[0]
            pre_r = 0
            for r in rocks:
                platform[pre_r:r, c] = np.sort(platform[pre_r:r, c])[::-1]
                pre_r = r + 1
            platform[pre_r:, c] = np.sort(platform[pre_r:, c])[::-1]
    elif direction == "W":
        # logger.debug("Tilting West")
        for r in range(len(platform)):
            rocks = np.where(platform[r, :] == "#")[0]
            pre_c = 0
            for c in rocks:
                platform[r, pre_c:c] = np.sort(platform[r, pre_c:c])[::-1]
                pre_c = c + 1
            platform[r, pre_c:] = np.sort(platform[r, pre_c:])[::-1]
    elif direction == "S":
        # logger.debug("Tilting South")
        for c in range(len(platform[0])):
            rocks = np.where(platform[:, c] == "#")[0]
            pre_r = len(platform) - 1
            for r in rocks[::-1]:
                platform[r + 1 : pre_r + 1, c] = np.sort(platform[r + 1 : pre_r + 1, c])
                pre_r = r - 1
            platform[: pre_r + 1, c] = np.sort(platform[: pre_r + 1, c])
    elif direction == "E":
        # logger.debug("Tilting East")
        for r in range(len(platform)):
            rocks = np.where(platform[r, :] == "#")[0]
            pre_c = len(platform[0]) - 1
            for c in rocks[::-1]:
                platform[r, c + 1 : pre_c + 1] = np.sort(platform[r, c + 1 : pre_c + 1])
                pre_c = c - 1
            platform[r, : pre_c + 1] = np.sort(platform[r, : pre_c + 1])
    else:
        raise ValueError(f"Unknown direction {direction}")

    return platform


def solver(args, logger):
    if args.test:
        lines = open("test_input.txt", "r").readlines()
    else:
        lines = open("input.txt", "r").readlines()

    platform = []
    for l in lines:
        row = np.array([c for c in l.strip()])
        platform.append(row)

    platform = np.array(platform)
    logger.debug(f"\n{platform}")
    result = 0

    if args.part == 1:
        platform = tilt(platform, "N", logger)
        logger.debug(f"\n{platform}")
        result = calculate_load(platform, logger)

    elif args.part == 2:
        round_rocks = np.where(platform == "O")
        logger.debug(f"round_rocks = {round_rocks}")
        loads = [calculate_load(platform, logger)]
        _cache = {}
        for c in range(1000000000):
            for d in ["N", "W", "S", "E"]:
                platform = tilt(platform, d, logger)

            loads.append(calculate_load(platform, logger))

            state = "".join("".join(row) for row in platform)
            try:
                result = _cache[hash(state)]
                logger.debug("cache hit")
                break
            except:
                _cache[hash(state)] = c

        logger.debug(f"loads = {loads}")

        first_repetition = _cache[hash(state)]
        cycle_length = c - first_repetition
        result = loads[
            first_repetition + (1000000000 - first_repetition) % cycle_length
        ]

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 14: Parabolic Reflector Dish "
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
