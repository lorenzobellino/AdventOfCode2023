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


def search_around(engine_schematic, r, c, rows, cols, logger):
    numbers = []
    for i in range(r - 1, r + 2):
        for j in range(c - 1, c + 2):
            if 0 <= i < rows and 0 <= j < cols and (i != r or j != c):
                if engine_schematic[i][j].isdigit():
                    begin = end = j
                    while engine_schematic[i][begin].isdigit():
                        begin -= 1
                        if begin < 0:
                            break
                    while engine_schematic[i][end].isdigit():
                        end += 1
                        if end >= cols:
                            break
                    n = int("".join(engine_schematic[i][begin + 1 : end]))
                    for k in range(begin + 1, end):
                        engine_schematic[i][k] = "."
                    numbers.append(n)
    return numbers


def solver(args, logger):
    lines = open("input.txt", "r").readlines()
    rows = len(lines)
    cols = len(lines[0].strip())
    result = 0
    engine_schematic = []
    for line in lines:
        engine_schematic.append([*line.strip()])

    if args.part == 1:
        for r in range(rows):
            for c in range(cols):
                if (
                    not engine_schematic[r][c].isdigit()
                    and engine_schematic[r][c] != "."
                ):
                    numbers = search_around(engine_schematic, r, c, rows, cols, logger)
                    result += sum(numbers)

    else:
        for r in range(rows):
            for c in range(cols):
                if (
                    not engine_schematic[r][c].isdigit()
                    and engine_schematic[r][c] == "*"
                ):
                    numbers = search_around(engine_schematic, r, c, rows, cols, logger)
                    if len(numbers) == 2:
                        result += numbers[0] * numbers[1]

    logger.debug(f"result: {result}")

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 3: Gear Ratios"
    )
    parser.add_argument(
        "-p",
        "--part",
        help="part of the challenge to solve (1 or 2)",
        type=int,
        choices=[1, 2],
        required=True,
    )
    args = parser.parse_args()
    logger_local.setLevel(level=logging.DEBUG if args.verbose else logging.INFO)

    ch = logging.StreamHandler()
    ch.setFormatter(CustomFormatter())

    logger_local.addHandler(ch)
    solution = solver(args, logger_local)
    logger_local.info(solution)
