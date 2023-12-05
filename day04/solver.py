#!/bin/python3.9
import argparse
import re
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
    lines = open("input.txt", "r").readlines()
    cards = dict()
    result = 0
    for l in lines:
        l = re.sub(r"\s+", " ", l)
        game_id, numbers = l.strip().split(":")
        _id = int(game_id.split(" ")[1])
        winning_number = numbers.split("|")[0].strip().split(" ")
        available_numbers = numbers.split("|")[1].strip().split(" ")
        cards[_id] = [winning_number, available_numbers, 1]

    if args.part == 1:
        for _id, card in cards.items():
            winning_number = set(card[0])
            available_numbers = set(card[1])
            winners = winning_number.intersection(available_numbers)
            result += int(2 ** (len(winners) - 1))

    else:
        for _id, card in cards.items():
            winning_number = set(card[0])
            available_numbers = set(card[1])
            winners = winning_number.intersection(available_numbers)
            for i in range(_id + 1, _id + len(winners) + 1):
                cards[i][2] += 1 * card[2]
            result += card[2]

    logger.debug(f"result: {result}")

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 4: Scratchcards"
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
