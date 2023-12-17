#!/bin/python3.9
import argparse
import logging

from collections import deque

import sys

# print(sys.getrecursionlimit())
# sys.setrecursionlimit(10000)

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


# def bounce_light(q, grid, energization, rec, _cache, logger):
#     if rec > 500:
#         return
#     if q.empty():
#         return
#     p = q.get()
#     x, y = p[0]
#     d = p[1]
#     if x >= len(grid[0]) or y >= len(grid) or x < 0 or y < 0:
#         bounce_light(q, grid, energization, rec, _cache, logger)
#         return
#     if energization[x][y] == 1:
#         # print("already energized")
#         rec += 1
#     energization[x][y] = 1

#     logger.debug(f"({x}, {y}) - {d} : {grid[x][y]}")

#     pp = "\n".join(["".join([str(_) for _ in l]) for l in energization])
#     logger.debug(f"\n{pp}\n")
#     ee = "\n".join(["".join([str(_) for _ in l]) for l in grid])
#     logger.debug(f"\n{ee}\n")
#     logger.debug(q.qsize())
#     # input()

#     p = []

#     if grid[x][y] == ".":
#         # p.append((x + d[0], y + d[1]))
#         p.append(((x + d[0], y + d[1]), d))
#         # logger.debug(f"point")
#         # input()
#     elif grid[x][y] == "|":
#         if d[0] == 0:
#             # p.append(((x + 1, y), (1, 0)))
#             # p.append(((x - 1, y), (-1, 0)))
#             p.append(((x + 1, y), (1, 0)))
#             p.append(((x - 1, y), (-1, 0)))
#         else:
#             # p.append(((x+d[0], y), d))
#             # p.append((x + d[0], y + d[1]))
#             p.append(((x + d[0], y + d[1]), d))
#     elif grid[x][y] == "-":
#         if d[1] == 0:
#             # p.append((x, y + 1))
#             # p.append((x, y - 1))
#             p.append(((x, y + 1), (0, 1)))
#             p.append(((x, y - 1), (0, -1)))
#         else:
#             # p.append((x + d[0], y + d[1]))
#             p.append(((x + d[0], y + d[1]), d))
#     elif grid[x][y] == "/":
#         if d == (0, 1):
#             # p.append((x - 1, y))
#             p.append(((x - 1, y), (-1, 0)))
#         elif d == (0, -1):
#             # p.append((x + 1, y))
#             p.append(((x + 1, y), (1, 0)))
#         elif d == (1, 0):
#             # p.append((x, y - 1))
#             p.append(((x, y - 1), (0, -1)))
#         elif d == (-1, 0):
#             # p.append((x, y + 1))
#             p.append(((x, y + 1), (0, 1)))
#     elif grid[x][y] == "\\":
#         if d == (0, 1):
#             # p.append((x + 1, y))
#             p.append(((x + 1, y), (1, 0)))
#         elif d == (0, -1):
#             # p.append((x - 1, y))
#             p.append(((x - 1, y), (-1, 0)))
#         elif d == (1, 0):
#             # p.append((x, y + 1))
#             p.append(((x, y + 1), (0, 1)))
#         elif d == (-1, 0):
#             # p.append((x, y - 1))
#             p.append(((x, y - 1), (0, -1)))
#     else:
#         logger.info("Unknown character")

#     for _p in p:
#         if _p not in _cache:
#             q.put((_p))
#             _cache.append(_p)
#         else:
#             logger.info(f"already in cache: {_p}")
#     # logger.info(f"c: {len(_cache)}")
#     bounce_light(q, grid, energization, rec, _cache, logger)


def new_cells(grid, x, y, d):
    if grid[x][y] == ".":
        return [((x + d[0], y + d[1]), d)]
    if grid[x][y] == "|":
        if d[0] == 0:
            return [((x + 1, y), (1, 0)), ((x - 1, y), (-1, 0))]
        else:
            return [((x + d[0], y + d[1]), d)]
    if grid[x][y] == "-":
        if d[1] == 0:
            return [((x, y + 1), (0, 1)), ((x, y - 1), (0, -1))]
        else:
            return [((x + d[0], y + d[1]), d)]
    if grid[x][y] == "/":
        if d == (0, 1):
            return [((x - 1, y), (-1, 0))]
        elif d == (0, -1):
            return [((x + 1, y), (1, 0))]
        elif d == (1, 0):
            return [((x, y - 1), (0, -1))]
        elif d == (-1, 0):
            return [((x, y + 1), (0, 1))]
    if grid[x][y] == "\\":
        if d == (0, 1):
            return [((x + 1, y), (1, 0))]
        elif d == (0, -1):
            return [((x - 1, y), (-1, 0))]
        elif d == (1, 0):
            return [((x, y + 1), (0, 1))]
        elif d == (-1, 0):
            return [((x, y - 1), (0, -1))]


def check_bounds(grid, c):
    p, d = c
    x, y = p
    if x >= len(grid[0]) or y >= len(grid) or x < 0 or y < 0:
        return False
    return True


def bounce_light(q, grid, energization, _cache, logger):
    while q:
        p, d = q.popleft()
        x, y = p

        _cache.append((p, d))
        energization[x][y] = 1

        cells = new_cells(grid, x, y, d)
        for c in cells:
            if c not in _cache and check_bounds(grid, c):
                _cache.append(c)
                q.append(c)

    return energization


def solver(args, logger):
    if args.test:
        lines = open("test_input.txt", "r").readlines()
    else:
        lines = open("input.txt", "r").readlines()

    grid = [[_ for _ in l.strip()] for l in lines]
    energization = [[0 for _ in l.strip()] for l in lines]

    g = "\n".join(["".join([str(_) for _ in l]) for l in grid])
    logger.debug(f"\n{g}\n")

    _cache = []
    result = 0

    if args.part == 1:
        q = deque()
        q.append(((0, 0), (0, 1)))
        energy = bounce_light(q, grid, energization, _cache, logger)
        result = sum([sum(l) for l in energy])

    elif args.part == 2:
        res = {}
        logger.info(f"top row")
        for y in range(len(grid)):
            logger.debug(f"y: {y}")
            q = deque()
            q.append(((0, y), (1, 0)))
            _cache = []
            energization = [[0 for _ in range(len(grid[0]))] for l in range(len(grid))]
            energy = sum(
                [sum(l) for l in bounce_light(q, grid, energization, _cache, logger)]
            )
            res[((0, y), (0, 1))] = energy
            pp = "\n".join(["".join([str(_) for _ in l]) for l in energization])
            logger.debug(f"\n{pp}\n{energy}")
        # print(len(res))
        # input()
        logger.info(f"bottom row")
        for y in range(len(grid)):
            logger.debug(f"y: {y}")
            q = deque()
            q.append(((len(grid[0]) - 1, y), (-1, 0)))
            _cache = []
            energization = [[0 for _ in range(len(grid[0]))] for l in range(len(grid))]
            energy = sum(
                [sum(l) for l in bounce_light(q, grid, energization, _cache, logger)]
            )
            res[((len(grid[0]) - 1, y), (0, -1))] = energy
            pp = "\n".join(["".join([str(_) for _ in l]) for l in energization])
            logger.debug(f"\n{pp}\n{energy}")

        # print(len(res))
        # input()
        logger.info(f"left column")
        for x in range(len(grid[0])):
            logger.debug(f"x: {x}")
            q = deque()
            q.append(((x, 0), (0, 1)))
            _cache = []
            energization = [[0 for _ in range(len(grid[0]))] for l in range(len(grid))]
            energy = sum(
                [sum(l) for l in bounce_light(q, grid, energization, _cache, logger)]
            )
            res[((x, 0), (1, 0))] = energy
            pp = "\n".join(["".join([str(_) for _ in l]) for l in energization])
            logger.debug(f"\n{pp}\n{energy}")

        # print(len(res))
        # input()
        logger.info(f"right column")

        for x in range(len(grid[0])):
            logger.debug(f"x: {x}")
            q = deque()
            q.append(((x, len(grid) - 1), (0, -1)))
            _cache = []
            energization = [[0 for _ in range(len(grid[0]))] for l in range(len(grid))]
            energy = sum(
                [sum(l) for l in bounce_light(q, grid, energization, _cache, logger)]
            )
            res[((x, len(grid) - 1), (-1, 0))] = energy
            pp = "\n".join(["".join([str(_) for _ in l]) for l in energization])
            logger.debug(f"\n{pp}\n{energy}")

        # print(len(res))
        # input()
        result = max([v for k, v in res.items()])
        # # result = res[max([k for k, v in res.items() if v == max_energy])]
        for k, v in res.items():
            logger.debug(f"{k} - {v}")

        # result = 2

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
