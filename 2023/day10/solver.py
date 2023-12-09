#!/bin/python3.9
import argparse
import logging

import numpy as np

from queue import PriorityQueue

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


mapping = {
    "S": [(0, 0), (0, 0)],
    "|": [(1, 0), (-1, 0)],
    "-": [(0, 1), (0, -1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(1, 0), (0, -1)],
    "F": [(1, 0), (0, 1)],
    ".": [(0, 0), (0, 0)],
}


def compute_intersection(maze, row, col):
    return (
        np.count_nonzero(maze[row][0:col] != "-")
        - np.count_nonzero(maze[row][0:col] == ".")
        - np.count_nonzero(maze[row][0:col] == "7")
        - np.count_nonzero(maze[row][0:col] == "F")
    )


def solver(args, logger):
    if args.test:
        lines = open("test_input.txt", "r").readlines()
    else:
        lines = open("input.txt", "r").readlines()

    maze = np.array([[c for c in l.strip()] for l in lines])
    maze_distance = np.array([[-1 for c in l.strip()] for l in lines])
    r = maze.shape[0]
    c = maze.shape[1]
    start = list(zip(*np.where(maze == "S")))[0]
    maze_distance[start] = 0
    q = PriorityQueue()
    connected = [
        tuple(map(sum, zip(start, i))) for i in [(-1, 0), (1, 0), (0, -1), (0, 1)]
    ]
    valid_connection = {
        (1, 0): ["|", "L", "J"],
        (-1, 0): ["|", "7", "F"],
        (0, -1): ["-", "L", "F"],
        (0, 1): ["-", "J", "7"],
    }
    for p, direction in zip(connected, [(-1, 0), (1, 0), (0, -1), (0, 1)]):
        if p[0] < 0 or p[0] >= r or p[1] < 0 or p[1] >= c:
            continue
        if maze[p] in valid_connection[direction]:
            q.put((1, p))
            maze_distance[p] = 1

    if args.part == 1:
        while not q.empty():
            current = q.get()
            logger.debug(f"current: {current}")
            connected = [
                tuple(map(sum, zip(current[1], i))) for i in mapping[maze[current[1]]]
            ]
            logger.debug(f"connected: {connected}")
            for p in connected:
                logger.debug(f"\tchecking p = {p}")
                if maze_distance[p] == -1:
                    q.put((current[0] + 1, p))
                    maze_distance[p] = current[0] + 1
            logger.debug(f"q: {q.queue}")
            logger.debug(f"maze_distance:\n{maze_distance}")

        result = np.max(maze_distance)

    elif args.part == 2:
        result = 0
        while not q.empty():
            current = q.get()
            connected = [
                tuple(map(sum, zip(current[1], i))) for i in mapping[maze[current[1]]]
            ]
            for p in connected:
                if maze_distance[p] == -1:
                    q.put((current[0] + 1, p))
                    maze_distance[p] = current[0] + 1

        logger.debug(f"maze_distance:\n{maze_distance}")

        maze_loop = np.array([["." for c in l.strip()] for l in lines])
        for i, rr in enumerate(maze_distance):
            for j, cc in enumerate(rr):
                if cc >= 0:
                    maze_loop[i, j] = maze[i, j]

        row = col = 0
        for row in range(r):
            for col in range(c):
                if maze_loop[row, col] == ".":
                    result += compute_intersection(maze_loop, row, col)

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 10: Pipe Maze"
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
