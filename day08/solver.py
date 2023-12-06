#!/bin/python3.9
import argparse
import logging
import re
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

    sequence = [1 if l == "R" else 0 for l in lines[0].strip()]
    lines.pop(0)
    lines.pop(0)
    mapping = dict()
    for l in lines:
        start, left, right = re.findall(r"\w+", l)
        mapping[start] = (left, right)

    logger.debug(f"sequence: {sequence}")
    logger.debug(f"mapping: {mapping}")

    if args.part == 1:
        element = "AAA"
        idx = 0
        while element != "ZZZ":
            instruction = sequence[idx % len(sequence)]
            element = mapping[element][instruction]
            idx += 1

        result = idx

    elif args.part == 2:
        logger.debug(f"len(sequence): {len(sequence)}")

        elements = [k for k in mapping.keys() if k[2] == "A"]
        len_seq = []
        for e in elements:
            logger.debug(f"e: {e}")
            elem = e
            idx = 0
            while elem[2] != "Z":
                instruction = sequence[idx % len(sequence)]
                elem = mapping[elem][instruction]
                idx += 1
            logger.debug(f"idx: {idx}")
            len_seq.append(idx)

        lcm = 1
        for i in len_seq:
            lcm = lcm * i // gcd(lcm, i)

        logger.debug(f"lcm: {lcm}")

        result = lcm

    # logger.debug(f"result: {result}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 8: Haunted Wasteland"
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
