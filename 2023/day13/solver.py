#!/bin/python3.9
import argparse
import logging
import numpy as np

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

    patterns = []
    p = []
    for l in lines:
        if not l.strip():
            patterns.append(np.array(p, dtype=bool))
            p = []
        else:
            p.append([1 if c == "#" else 0 for c in l.strip()])
    patterns.append(np.array(p, dtype=bool))

    result = 0

    if args.part == 1:
        for p in patterns:
            logger.debug("new pattern")
            # check for vertical symmetry

            for i in range(1, len(p[0] - 1)):
                p1 = p[:, 0 if i * 2 < len(p[0]) else (i - (len(p[0]) - i)) : i]
                p2 = p[:, i : i * 2 if i * 2 < len(p[0]) else len(p[0])]
                reflection = p1 == np.fliplr(p2)

                if reflection.all():
                    logger.debug(f"found vertical symmetry at {i}\n")
                    result += i

            # check for horizontal symmetry

            for i in range(1, len(p)):
                p1 = p[0 if i * 2 < len(p) else (i - (len(p) - i)) : i, :]
                p2 = p[i : i * 2 if i * 2 < len(p) else len(p), :]

                reflection = p1 == np.flipud(p2)
                if reflection.all():
                    logger.debug(f"found horizontal symmetry at {i}\n")
                    result += i * 100

    elif args.part == 2:
        for p in patterns:
            logger.debug("new pattern")
            # check for vertical symmetry

            for i in range(1, len(p[0] - 1)):
                p1 = p[:, 0 if i * 2 < len(p[0]) else (i - (len(p[0]) - i)) : i]
                p2 = p[:, i : i * 2 if i * 2 < len(p[0]) else len(p[0])]
                reflection = p1 == np.fliplr(p2)

                if sum(sum(np.invert(reflection))) == 1:
                    logger.debug(f"found vertical smudged symmetry at {i}\n")
                    result += i
            # check for horizontal symmetry

            for i in range(1, len(p)):
                p1 = p[0 if i * 2 < len(p) else (i - (len(p) - i)) : i, :]
                p2 = p[i : i * 2 if i * 2 < len(p) else len(p), :]

                reflection = p1 == np.flipud(p2)

                if sum(sum(np.invert(reflection))) == 1:
                    logger.debug(f"found horizontal smudged symmetry at {i}\n")
                    result += i * 100

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 13: Point of Incidence "
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
