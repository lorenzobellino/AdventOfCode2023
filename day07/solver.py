#!/bin/python3.9
import argparse
import logging


logger_local = logging.getLogger("day01")

rankings = {
    1: "high card",
    2: "pair",
    3: "two pairs",
    4: "three of a kind",
    5: "full house",
    6: "four of a kind",
    7: "five of a kind",
}


class PokerHand_part1(object):
    def __init__(self, hand, bid):
        VALUES = {
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9,
            "T": 10,
            "J": 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
        self.hand = hand
        self.cards = [c for c in hand]
        self.values = [VALUES[self.cards[i]] for i in range(len(self.cards))]
        self.og_values = self.values.copy()
        self.values.sort(reverse=True)
        self.bid = int(bid)
        self.rank = self.get_rank()

    def __repr__(self):
        return f"{self.hand} - {self.bid}"

    def __str__(self):
        return f"{self.hand} - {self.bid} - {self.rank}: {rankings[self.rank]}"

    def is_five_of_a_kind(self):
        return len(set(self.values)) == 1

    def is_four_of_a_kind(self):
        unique = list(set(self.values))
        return len(unique) == 2 and (
            self.values.count(unique[0]) == 4 or self.values.count(unique[-1]) == 4
        )

    def is_three_of_a_kind(self):
        unique = list(set(self.values))
        return len(unique) == 3 and (
            self.values.count(unique[0]) == 3
            or self.values.count(unique[1]) == 3
            or self.values.count(unique[2]) == 3
        )

    def is_full_house(self):
        unique = list(set(self.values))
        return len(unique) == 2 and (
            self.values.count(unique[0]) == 3 or self.values.count(unique[-1]) == 3
        )

    def is_two_pairs(self):
        unique = list(set(self.values))
        return len(unique) == 3 and (
            self.values.count(unique[0]) == 2
            or self.values.count(unique[1]) == 2
            or self.values.count(unique[2]) == 2
        )

    def is_pair(self):
        unique = list(set(self.values))
        return len(unique) == 4 and (
            self.values.count(unique[0]) == 2
            or self.values.count(unique[1]) == 2
            or self.values.count(unique[2]) == 2
            or self.values.count(unique[3]) == 2
        )

    def get_rank(self):
        if self.is_five_of_a_kind():
            return 7
        elif self.is_four_of_a_kind():
            return 6
        elif self.is_full_house():
            return 5
        elif self.is_three_of_a_kind():
            return 4
        elif self.is_two_pairs():
            return 3
        elif self.is_pair():
            return 2
        else:
            return 1

    def __lt__(self, other):
        if self.rank < other.rank:
            return True
        elif self.rank == other.rank:
            for i in range(len(self.values)):
                if not self.og_values[i] == other.og_values[i]:
                    return self.og_values[i] < other.og_values[i]
            return False

    def __eq__(self, other):
        return self.hand == other.hand


class PokerHand_part2(object):
    def __init__(self, hand, bid):
        VALUES = {
            "J": 2,
            "2": 3,
            "3": 4,
            "4": 5,
            "5": 6,
            "6": 7,
            "7": 8,
            "8": 9,
            "9": 10,
            "T": 11,
            "Q": 12,
            "K": 13,
            "A": 14,
        }
        self.hand = hand
        self.cards = [c for c in hand]
        self.values = [VALUES[self.cards[i]] for i in range(len(self.cards))]
        self.og_values = self.values.copy()
        self.values.sort(reverse=True)
        self.bid = int(bid)
        self.rank = self.get_rank()

    def __repr__(self):
        return f"{self.hand} - {self.bid}"

    def __str__(self):
        return f"{self.hand} - {self.bid:5d} - {self.rank}: {rankings[self.rank]}"

    def is_five_of_a_kind(self):
        return (2 in self.values and len(set(self.values)) == 2) or (
            len(set(self.values)) == 1
        )

    def is_four_of_a_kind(self):
        unique = list(set(self.values))
        if 2 not in unique:
            return len(unique) == 2 and (
                self.values.count(unique[0]) == 4 or self.values.count(unique[-1]) == 4
            )
        else:
            J = self.values.count(2)
            unique.remove(2)
            counts = [self.values.count(c) for c in unique]
            return max(counts) + J >= 4

    def is_three_of_a_kind(self):
        unique = list(set(self.values))
        if 2 not in unique:
            return len(unique) == 3 and (
                self.values.count(unique[0]) == 3
                or self.values.count(unique[1]) == 3
                or self.values.count(unique[2]) == 3
            )
        else:
            J = self.values.count(2)
            unique.remove(2)
            counts = [self.values.count(c) for c in unique]
            return max(counts) + J >= 3

    def is_full_house(self):
        unique = list(set(self.values))
        if 2 not in unique:
            return len(unique) == 2 and (
                self.values.count(unique[0]) == 3 or self.values.count(unique[-1]) == 3
            )
        else:
            J = self.values.count(2)
            unique.remove(2)
            counts = [self.values.count(c) for c in unique]
            return len(counts) == 2

    def is_two_pairs(self):
        unique = list(set(self.values))
        if 2 not in unique:
            return len(unique) == 3 and (
                self.values.count(unique[0]) == 2
                or self.values.count(unique[1]) == 2
                or self.values.count(unique[2]) == 2
            )
        else:
            J = self.values.count(2)
            unique.remove(2)
            counts = [self.values.count(c) for c in unique]
            return (max(counts) == 2 and J == 1) or (max(counts) == 1 and J == 2)

    def is_pair(self):
        unique = list(set(self.values))
        return (
            len(unique) == 4
            and (
                self.values.count(unique[0]) == 2
                or self.values.count(unique[1]) == 2
                or self.values.count(unique[2]) == 2
                or self.values.count(unique[3]) == 2
            )
            or (2 in unique)
        )

    def get_rank(self):
        if self.is_five_of_a_kind():
            return 7
        elif self.is_four_of_a_kind():
            return 6
        elif self.is_full_house():
            return 5
        elif self.is_three_of_a_kind():
            return 4
        elif self.is_two_pairs():
            return 3
        elif self.is_pair():
            return 2
        else:
            return 1

    def __lt__(self, other):
        if self.rank < other.rank:
            return True
        elif self.rank == other.rank:
            for i in range(len(self.values)):
                if not self.og_values[i] == other.og_values[i]:
                    return self.og_values[i] < other.og_values[i]
            return False

    def __eq__(self, other):
        return self.hand == other.hand


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
    result = []
    hands = []

    if args.test:
        lines = open("test_input.txt", "r").readlines()
    else:
        lines = open("input.txt", "r").readlines()

    if args.part == 1:
        for l in lines:
            hand, bid = l.strip().split(" ")
            hands.append(PokerHand_part1(hand, bid))
        sorted_hands = sorted(hands)
        result = [h.bid * (i + 1) for i, h in enumerate(sorted_hands)]

    elif args.part == 2:
        for l in lines:
            hand, bid = l.strip().split(" ")
            hands.append(PokerHand_part2(hand, bid))
        sorted_hands = sorted(hands)
        result = [h.bid * (i + 1) for i, h in enumerate(sorted_hands)]
        for i, h in enumerate(sorted_hands):
            logger.debug(f"{i + 1:4d}:  {h}")

    # logger.debug(f"result: {result}")
    return sum(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 7: Camel Cards"
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
