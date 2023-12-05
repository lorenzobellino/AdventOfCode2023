#!/bin/python3.9
import argparse
from math import inf
from collections import namedtuple

orderd_map = {
    0: "seed-to-soli",
    1: "soil-to-fertilizer",
    2: "fertilizer-to-water",
    3: "water-to-light",
    4: "light-to-temperature",
    5: "temperature-to-humidity",
    6: "humidity-to-location",
}


def overlap(range1, range2):
    return not (range1.start >= range2.stop or range1.stop < range2.start)


def map_s_d(seed_range, mapping, mapping_id, j):
    tail = None
    new_seed_range_list = []
    if seed_range.start >= mapping[mapping_id][j].source_range.start:
        if seed_range.stop <= mapping[mapping_id][j].source_range.stop:
            # fully contained
            new_seed_range_list.append(
                range(
                    seed_range.start + mapping[mapping_id][j].delta,
                    seed_range.stop + mapping[mapping_id][j].delta,
                )
            )
        elif seed_range.stop > mapping[mapping_id][j].source_range.stop:
            # nothing preceeding
            # seed_range tail not contained
            new_seed_range_list.append(
                range(
                    seed_range.start + mapping[mapping_id][j].delta,
                    mapping[mapping_id][j].source_range.stop
                    + mapping[mapping_id][j].delta,
                )
            )
            tail = range(mapping[mapping_id][j].source_range.stop, seed_range.stop)
    elif seed_range.start < mapping[mapping_id][j].source_range.start:
        if seed_range.stop <= mapping[mapping_id][j].source_range.stop:
            # seed_range head not contained
            # print("seed_range head not contained")
            head = range(seed_range.start, mapping[mapping_id][j].source_range.start)
            new_seed_range_list.append(head)
            new_seed_range_list.append(
                range(
                    mapping[mapping_id][j].source_range.start
                    + mapping[mapping_id][j].delta,
                    seed_range.stop + mapping[mapping_id][j].delta,
                )
            )
        elif seed_range.stop > mapping[mapping_id][j].source_range.stop:
            # seed_range head not contained
            # seed_range tail not contained
            new_seed_range_list.append(
                range(
                    mapping[mapping_id][j].source_range.start
                    + mapping[mapping_id][j].delta,
                    mapping[mapping_id][j].source_range.stop
                    + mapping[mapping_id][j].delta,
                )
            )
            tail = range(mapping[mapping_id][j].source_range.stop, seed_range.stop)
    else:
        raise ValueError("Something went wrong")
    if tail is not None:
        try:
            source_range = mapping[mapping_id][j + 1].source_range
            overlap_found = overlap(tail, source_range)
        except IndexError:
            overlap_found = False

        if overlap_found:
            new_seed_range_list += map_s_d(tail, mapping, mapping_id, j + 1)
        else:
            new_seed_range_list.append(
                range(
                    tail.start,
                    tail.stop,
                )
            )
    new_seed_range_list = sorted(new_seed_range_list, key=lambda x: x.start)
    return new_seed_range_list


def map_source_to_destination_r(seed_range_list, mapping, mapping_id):
    if seed_range_list is None:
        return inf
    if mapping_id >= len(mapping):
        return seed_range_list[0].start
    r = inf

    new_seed_range_list = []
    for seed_range in seed_range_list:
        i = 0

        while mapping[mapping_id][i].source_range.stop <= seed_range.start:
            i += 1
            if i >= len(mapping[mapping_id]):
                break
        if (
            i == len(mapping[mapping_id])
            or mapping[mapping_id][i].source_range.start >= seed_range.stop
        ):
            new_seed_range_list.append(seed_range)

        else:
            new_seed_range_list += map_s_d(seed_range, mapping, mapping_id, i)
    new_seed_range_list = sorted(new_seed_range_list, key=lambda x: x.start)
    r = map_source_to_destination_r(new_seed_range_list, mapping, mapping_id + 1)
    return r


def solver(args):
    if args.test:
        lines = open("test_input.txt", "r").readlines()
    else:
        lines = open("input.txt", "r").readlines()

    mapping = dict()
    mapping_id = 0
    result = inf
    mapping_range = namedtuple(
        "mapping_range", ["destination_range", "source_range", "range_length", "delta"]
    )

    if args.part == 1:
        seeds = [int(s) for s in lines.pop(0).split(":")[1].strip().split(" ")]
        lines.pop(0)
        mapped_output = []
        while True:
            try:
                l = lines.pop(0)
            except IndexError:
                break
            if l[0].isalpha():
                mapping[mapping_id] = []
            else:
                while l[0].isdigit():
                    tmp = tuple(int(_) for _ in l.strip().split(" "))
                    destination_start = tmp[0]
                    source_start = tmp[1]
                    _lenght = tmp[2]
                    destination_range = range(
                        destination_start, destination_start + _lenght
                    )
                    source_range = range(source_start, source_start + _lenght)
                    range_length = tmp[2]
                    delta = tmp[0] - tmp[1]
                    mapping[mapping_id].append(
                        (destination_range, source_range, range_length, delta)
                    )
                    try:
                        l = lines.pop(0)
                    except IndexError:
                        break
                mapping_id += 1

        for s in seeds:
            n = s
            for k, v in mapping.items():
                for _range in v:
                    if n in _range[1]:
                        n += _range[3]
                        break
            if n < result:
                result = n

    elif args.part == 2:
        s = (int(_) for _ in lines.pop(0).split(":")[1].strip().split(" "))
        seeds = []
        for n in iter(s):
            range_start = n
            range_length = next(s)
            seeds.append(range(range_start, range_start + range_length))
        lines.pop(0)
        while True:
            try:
                l = lines.pop(0)

            except IndexError:
                break
            if l[0].isalpha():
                mapping[mapping_id] = []
            else:
                while l[0].isdigit():
                    tmp = tuple(int(_) for _ in l.strip().split(" "))
                    destination_start = tmp[0]
                    source_start = tmp[1]
                    _lenght = tmp[2]
                    destination_range = range(
                        destination_start, destination_start + _lenght
                    )
                    source_range = range(source_start, source_start + _lenght)
                    range_length = tmp[2]
                    delta = tmp[0] - tmp[1]

                    mapping[mapping_id].append(
                        mapping_range(
                            destination_range, source_range, range_length, delta
                        )
                    )
                    try:
                        l = lines.pop(0)
                    except IndexError:
                        break
                mapping[mapping_id] = sorted(
                    mapping[mapping_id], key=lambda x: x.source_range.stop
                )
                mapping_id += 1

        mapped_output = []
        for seed_range in seeds:
            mapped_output.append(map_source_to_destination_r([seed_range], mapping, 0))

        result = min(mapped_output)

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code 2023 - Day 5: If You Give A Seed A Fertilizer"
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
    solution = solver(args)
    print(solution)
