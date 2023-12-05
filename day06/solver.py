#!/bin/python3.9
import argparse
import re
import numpy as np
from math import inf, ceil, floor
from collections import namedtuple
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


def solver(args, logger):
    result = []

    if args.test:
        lines = open("test_input.txt", "r").readlines()
    else:
        lines = open("input.txt", "r").readlines()

    races = dict()
    for l in lines:
        races[l.strip().split(":")[0]] = [
            int(_) for _ in re.findall(f"\d+", l.strip().split(":")[1])
        ]

    logger.debug(f"races : {races}")

    if args.part == 1:
        for time, distance in zip(races["Time"], races["Distance"]):
            a, b, c = -1, time, -distance
            delta = b**2 - 4 * a * c
            if delta < 0:
                logger.debug(f"delta < 0 -> no intersection")
            elif delta == 0:
                logger.debug(f"delta == 0 -> 1 intersection")
                intersection = (-b) / (2 * a)
                logger.debug(f"r: {intersection}")
            else:
                logger.debug(f"delta > 0 -> 2 intersections")
                intersection_1 = (-b + delta**0.5) / (2 * a)
                intersection_2 = (-b - delta**0.5) / (2 * a)
                if floor(intersection_1) == ceil(intersection_1):
                    intersection_1 += 1
                if floor(intersection_2) == ceil(intersection_2):
                    intersection_2 -= 1
                logger.debug(f"r1: {intersection_1}")
                logger.debug(f"r2: {intersection_2}")
                possibile_values = range(
                    ceil(intersection_1), floor(intersection_2) + 1
                )
                logger.debug(f"possibile_values: {possibile_values}")
                result.append(len(possibile_values))

    elif args.part == 2:
        time = int(lines[0].strip().split(":")[1].replace(" ", ""))
        distance = int(lines[1].strip().split(":")[1].replace(" ", ""))
        logger.debug(f"time: {time}")
        logger.debug(f"distance: {distance}")
        a, b, c = -1, time, -distance
        delta = b**2 - 4 * a * c
        if delta < 0:
            logger.debug(f"delta < 0 -> no intersection")
        elif delta == 0:
            logger.debug(f"delta == 0 -> 1 intersection")
            intersection = (-b) / (2 * a)
            logger.debug(f"r: {intersection}")
        else:
            logger.debug(f"delta > 0 -> 2 intersections")
            intersection_1 = (-b + delta**0.5) / (2 * a)
            intersection_2 = (-b - delta**0.5) / (2 * a)
            if floor(intersection_1) == ceil(intersection_1):
                intersection_1 += 1
            if floor(intersection_2) == ceil(intersection_2):
                intersection_2 -= 1
            logger.debug(f"r1: {intersection_1}")
            logger.debug(f"r2: {intersection_2}")
            possibile_values = range(ceil(intersection_1), floor(intersection_2) + 1)
            logger.debug(f"possibile_values: {possibile_values}")
            result.append(len(possibile_values))

    logger.debug(f"result: {result}")
    logger.debug(f"result: {np.prod(result)}")
    return np.prod(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 5: If You Give A Seed A Fertilizer"
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
