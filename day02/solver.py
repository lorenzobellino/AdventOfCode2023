#!/bin/python3.9
import re
import argparse

from collections import namedtuple

from math import inf

configuration = {
    "red": 12,
    "blue": 14,
    "green": 13,
}

colors = set(["red", "green", "blue"])

Record = namedtuple("record", ["red","green","blue"])


def solver(args):
    lines = open("input.txt", "r").readlines()
    games = {int(l.split(":")[0].split()[1]): [] for l in lines}
    result = 0
    for id,game in enumerate(lines):
        extractions = game.split(":")[1].split(";")
        for e in extractions:
            if e.strip() != "":
                r_dict = {v: int(k) for k,v in re.findall(r"(\d+) (\w+)", e)}
                diff = colors - set(r_dict.keys())
                while len(diff) > 0:
                    r_dict[diff.pop()] = 0
                r = Record(**r_dict)
                games[id+1].append(r)
    if args.part == 1:
        np = []
        p = []
        for id,g in games.items():
            possible = True

            for r in g:
                if r.red > configuration["red"] or r.green > configuration["green"] or r.blue > configuration["blue"]:
                    possible = False
                    np.append(id)
                    break
            if possible:
                p.append(id)
                result += id

        print(f"Possible: {p}")
        print(f"Not Possible: {np}")
        print(f"Result: {result}")  
        print(f"len(p): {len(p)}")
        print(f"len(np): {len(np)}")
        print(f"len : {len(p)+len(np)}")

    else:
        for id,g in games.items():
            minimum_configuration = Record(red=0,green=0,blue=0)
            for r in g:
                
                if r.red > minimum_configuration.red:
                    minimum_configuration = minimum_configuration._replace(red=r.red)
                if r.green > minimum_configuration.green:
                    minimum_configuration = minimum_configuration._replace(green=r.green)
                if r.blue > minimum_configuration.blue:
                    minimum_configuration = minimum_configuration._replace(blue=r.blue)
            print(f"Game {id}: {minimum_configuration} -> {minimum_configuration.red * minimum_configuration.green * minimum_configuration.blue}")
            result += minimum_configuration.red * minimum_configuration.green * minimum_configuration.blue

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
    args = parser.parse_args()
    solution = solver(args)
    print(solution)
