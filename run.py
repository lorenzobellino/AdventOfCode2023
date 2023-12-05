#!/bin/python

import argparse
import logging
import time
import os
import importlib

logger = logging.getLogger("AoC2023")


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


def run_challenge(args, logger):
    name = f"day{args.day:02d}.solver"
    os.chdir(f"day{args.day:02d}")
    logger.info(f"Running {name} part {args.part}")
    main_module = importlib.import_module(name)
    solver = getattr(main_module, "solver")
    solution = solver(args, logger)
    logger.info(f"Solution: {solution}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2023")
    parser.add_argument(
        "-d",
        "--day",
        help="Day of the challenge to solve",
        type=int,
        choices=range(1, 26),
        required=True,
        metavar="{1..25}",
    )
    parser.add_argument(
        "-p",
        "--part",
        help="Part of the challenge to solve (1 or 2)",
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
        help="Test mode - run challeng on test_input.txt",
        action="store_true",
    )
    args = parser.parse_args()
    logger.setLevel(level=logging.DEBUG if args.verbose else logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(level=logging.DEBUG if args.verbose else logging.INFO)
    # formatter = logging.Formatter("%(levelname)s - %(message)s")
    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)

    start = time.time()

    run_challenge(args, logger)

    end = time.time()
    logger.info(f"Elapsed time: {round(end - start, 2)}")
