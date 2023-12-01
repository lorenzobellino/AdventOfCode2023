#!/bin/python3.9
import re
import argparse

mapping = {
    "one": "o1e",
    "two": "t2o",
    "three": "thr3e",
    "four": "f4ur",
    "five": "fi5e",
    "six": "s6x",
    "seven": "s7ven",
    "eight": "e8ght",
    "nine": "n9ne",
}


def solver(args):
    lines = open("puzzle.txt", "r").readlines()
    if args.part == 2:
        for m in mapping:
            lines = [l.replace(m, mapping[m]) for l in lines]

    matches = [re.findall(r"\d", line) for line in lines]
    matches = [int(m[0]) * 10 + int(m[-1]) for m in matches]

    return sum(matches)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 1: Trebuchet?!"
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
    solution = solver(args)
    print(solution)
