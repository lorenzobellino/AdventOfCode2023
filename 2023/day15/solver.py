#!/bin/python3.9
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


def _hash(s):
    h = 0
    for c in s:
        h = ((h + ord(c)) * 17) % 256
    return h


def _print(boxes, lenses, label, value, s, logger):
    logger.debug(f'After "{s}":')
    for i, b in enumerate(boxes):
        if boxes[b]:
            s = f"Box {i}: "
            for j in range(len(boxes[b])):
                s += f" [{boxes[b][j]} {lenses[boxes[b][j]]}]"

            logger.debug(f"{s}")
    logger.debug("\n")


def solver(args, logger):
    if args.test:
        lines = open("test_input.txt", "r").readlines()
    else:
        lines = open("input.txt", "r").readlines()

    strings = [l.strip() for l in lines[0].split(",")]

    result = 0

    boxes = {i: [] for i in range(256)}
    lenses = {}

    if args.part == 1:
        for s in strings:
            logger.debug(f"{s} -> {_hash(s)}")
            result += _hash(s)

    elif args.part == 2:
        for s in strings:
            if "=" in s:
                label, value = s.split("=")
                box_id = _hash(label)
                if label not in boxes[box_id]:
                    boxes[box_id].append(label)
                lenses[label] = value
            else:
                label, value = s.split("-")
                box_id = _hash(label)
                if label in boxes[box_id]:
                    boxes[box_id].remove(label)
            if args.verbose:
                _print(boxes, lenses, label, value, s, logger)

        for i, b in enumerate(boxes):
            if boxes[b]:
                for j, l in enumerate(boxes[b]):
                    result += (i + 1) * (j + 1) * int(lenses[l])

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 15: Lens Library "
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
