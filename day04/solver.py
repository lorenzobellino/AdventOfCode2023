#!/bin/python3.9
import argparse
import re


def solver(args):
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
    solution = solver(args)
    print(solution)
