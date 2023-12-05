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


def map_source_destination(source_range, mapping, mapping_id):
    result_mapping = None
    founded_overlap = False

    if source_range == None:
        return None
    if mapping_id == len(mapping):
        return source_range.start

    # print(f"source_range: {source_range}")
    for _range in mapping[mapping_id]:
        # print(f"_range: {_range}")
        # input()
        # print(f"mapping : {mapping[mapping_id]}")
        overlap_range = range(
            max(_range.source_range.start, source_range.start),
            min(_range.source_range.stop, source_range.stop),
        )

        if overlap_range.start > overlap_range.stop:
            overlap_range = None
        # print(f"overlap_range: {overlap_range}")
        # print(f"source_range: {source_range}")
        # input()
        if overlap_range:
            founded_overlap = True
            # chek if overlap is all inside source_range
            # if not split in different searches

            print(f"{' '*mapping_id}overlap_range: {overlap_range}")
            print(f"{' '*mapping_id}source_range: {source_range}")
            print(f"{' '*mapping_id}mapping_source : {_range.source_range}")
            print(f"{' '*mapping_id}mapping_destination : {_range.destination_range}")
            print(f"{' '*mapping_id}mapping_delta : {_range.delta}")

            if (
                source_range.start >= overlap_range.start
                and source_range.stop <= overlap_range.stop
            ):
                # source range is contained in overlap range
                # print("source range is contained in overlap range")
                new_range1 = range(
                    source_range.start + _range.delta,
                    source_range.stop + _range.delta,
                )
                new_range2 = None
                new_range3 = None
            elif source_range.start < overlap_range.start:
                # source range start before overlap range
                # print("source range start before overlap range")
                if source_range.stop <= overlap_range.stop:
                    # source range stop before overlap range
                    new_range1 = range(source_range.start, overlap_range.start)
                    new_range2 = range(
                        overlap_range.start + _range.delta,
                        source_range.stop + _range.delta,
                    )
                    new_range3 = None
                else:
                    # source range stop after overlap range
                    # print("source range stop after overlap range")
                    new_range1 = range(source_range.start, overlap_range.start)
                    new_range2 = range(
                        overlap_range.start + _range.delta,
                        overlap_range.stop + _range.delta,
                    )
                    new_range3 = range(overlap_range.stop, source_range.stop)
            else:
                # source range start at overlap range start
                # print("source range start at overlap range start")
                if source_range.stop <= overlap_range.stop:
                    # source range stop before overlap range
                    new_range1 = None
                    new_range2 = range(
                        overlap_range.start + _range.delta,
                        source_range.stop + _range.delta,
                    )
                    new_range3 = range(source_range.stop, overlap_range.stop)
                else:
                    # source range stop after overlap range
                    # print("source range stop after overlap range")
                    new_range1 = None
                    new_range2 = range(
                        overlap_range.start + _range.delta,
                        overlap_range.stop + _range.delta,
                    )
                    new_range3 = range(overlap_range.stop, source_range.stop)
                # new_range1 = None
                # new_range2 = range(
                #     source_range.start + _range.delta,
                #     source_range.stop + _range.delta,
                # )
                # new_range3 = None

            print(f"{' '*mapping_id}new_range1: {new_range1}")
            print(f"{' '*mapping_id}new_range2: {new_range2}")
            print(f"{' '*mapping_id}new_range3: {new_range3}")
            # input()

            r1 = map_source_destination(new_range1, mapping, mapping_id + 1)
            r2 = map_source_destination(new_range2, mapping, mapping_id + 1)
            r3 = map_source_destination(new_range3, mapping, mapping_id + 1)

            print(f"{' '*mapping_id}mapping_id: {mapping_id}")
            print(f"{' '*mapping_id}\tr1: {r1}")
            print(f"{' '*mapping_id}\tr2: {r2}")
            print(f"{' '*mapping_id}\tr3: {r3}")
            # input()

            rr = [r for r in [r1, r2, r3] if r is not None]
            # if rr:
            r = min([r for r in rr])
            # else:
            # r = None

            # print(f"source : {source_range}\ndestination : {new_range}\n")
            # r = map_source_destination(new_range, mapping, mapping_id + 1)
            break

        # else:
        #     # print("no overlap")
        #     print(f"source : {source_range}\ndestination : {source_range}\n")
        #     r = map_source_destination(source_range, mapping, mapping_id + 1)
        # input()
    if not founded_overlap:
        print(f"{' '*mapping_id}no overlap")
        print(
            f"{' '*mapping_id}source : {source_range}\ndestination : {source_range}\n"
        )
        r = map_source_destination(source_range, mapping, mapping_id + 1)

    if result_mapping is None or r < result_mapping:
        result_mapping = r
    # else:
    #     if r.start < result_mapping.start:
    #         result_mapping = r
    # print(f"result_mapping: {result_mapping}")
    # input()
    return result_mapping


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
        while True:
            try:
                l = lines.pop(0)
                # print(f"line : {l}")
                # input()
            except IndexError:
                break
            if l[0].isalpha():
                mapping[mapping_id] = []
                # l = lines.pop(0)
                # print("l is alpha")
            else:
                while l[0].isdigit():
                    tmp = tuple(int(_) for _ in l.strip().split(" "))
                    # destination_range, source_range, range_length = tmp
                    destination_start = tmp[0]
                    source_start = tmp[1]
                    _lenght = tmp[2]
                    destination_range = range(
                        destination_start, destination_start + _lenght
                    )
                    source_range = range(source_start, source_start + _lenght)
                    range_length = tmp[2]
                    delta = tmp[0] - tmp[1]
                    # print(destination_range, source_range, range_length)
                    # input()
                    mapping[mapping_id].append(
                        (destination_range, source_range, range_length, delta)
                    )
                    try:
                        l = lines.pop(0)
                    except IndexError:
                        break
                mapping_id += 1

            # for k, v in mapping.items():
            #     print(f"{orderd_map[k]}: {v}")

            # input()

        # print(seeds)
        # print(f"len seeds: {len(seeds)}")
        # input()

        for s in seeds:
            n = s
            # print(f"seed: {n}")
            for k, v in mapping.items():
                # print(f"{orderd_map[k]}: {v}")
                for _range in v:
                    if n in _range[1]:
                        # print(f"{k}: {n} in {_range[1]}")
                        # print(f"delta : {_range[3]}")
                        n += _range[3]
                        # print(f"{k}: new number is {n}")
                        break
            # input()
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
        # print(f"seeds: {seeds}")
        while True:
            try:
                l = lines.pop(0)
                # print(f"line : {l}")
                # input()
            except IndexError:
                break
            if l[0].isalpha():
                mapping[mapping_id] = []
                # l = lines.pop(0)
                # print("l is alpha")
            else:
                while l[0].isdigit():
                    tmp = tuple(int(_) for _ in l.strip().split(" "))
                    # destination_range, source_range, range_length = tmp
                    destination_start = tmp[0]
                    source_start = tmp[1]
                    _lenght = tmp[2]
                    destination_range = range(
                        destination_start, destination_start + _lenght
                    )
                    source_range = range(source_start, source_start + _lenght)
                    range_length = tmp[2]
                    delta = tmp[0] - tmp[1]
                    # print(destination_range, source_range, range_length)
                    # input()
                    mapping[mapping_id].append(
                        mapping_range(
                            destination_range, source_range, range_length, delta
                        )
                    )
                    try:
                        l = lines.pop(0)
                    except IndexError:
                        break
                mapping_id += 1
        # print(f"mapping : {mapping}")
        # for k, v in mapping.items():
        #     print(f"{orderd_map[k]}: {v}")

        for sr in seeds:
            output_range = map_source_destination(sr, mapping, 0)
            print(f"output_range: {output_range}\n\n\n")
            input()
            if output_range is not None:
                if output_range < result:
                    result = output_range

            # input()

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


#         list_of_seeds = (int(s) for s in lines.pop(0).split(":")[1].strip().split(" "))
#         seeds = []
#         for n in iter(list_of_seeds):
#             range_start = n
#             range_length = next(list_of_seeds)
#             seeds.append(range(range_start, range_start + range_length))
#         lines.pop(0)
#         print("completed seeds ranges")
#         while True:
#             try:
#                 l = lines.pop(0)
#             except IndexError:
#                 break
#             if l[0].isalpha():
#                 mapping[mapping_id] = []
#             else:
#                 while l[0].isdigit():
#                     tmp = tuple(int(_) for _ in l.strip().split(" "))
#                     destination_start = tmp[0]
#                     source_start = tmp[1]
#                     _lenght = tmp[2]
#                     destination_range = range(
#                         destination_start, destination_start + _lenght
#                     )
#                     source_range = range(source_start, source_start + _lenght)
#                     range_length = tmp[2]
#                     delta = tmp[0] - tmp[1]
#                     mapping[mapping_id].append(
#                         (destination_range, source_range, range_length, delta)
#                     )
#                     try:
#                         l = lines.pop(0)
#                     except IndexError:
#                         break
#                 mapping_id += 1

#         print("completed mapping")

#         ranges_to_check = {k: [] for k in range(len(seeds))}
#         for _id, seed_range in enumerate(seeds):
#             for k, v in mapping.items():
#                 for _range in v:
#                     new_range = range(
#                         max(_range[1].start, seed_range.start),
#                         min(_range[1].stop, seed_range.stop),
#                     )
#                     if new_range:
#                         ranges_to_check[_id].append(new_range)
#                     # print(f"ranges_to_check: {ranges_to_check}")
#                     # input()
#         seeds_r = {k: [] for k in range(len(seeds))}
#         print("completed ranges_to_check")
#         for k, v in ranges_to_check.items():
#             # print(f"{k}: {v}")
#             print(f"k is {k}")
#             seed_start = inf
#             seed_stop = 0
#             for r in v:
#                 if r.start < seed_start:
#                     seed_start = r.start
#                 if r.stop > seed_stop:
#                     seed_stop = r.stop
#             seeds_r[k] = range(seed_start, seed_stop)
#             # print(f"{k}: {seeds_r[k]}")
#             # input()
#         print("completed seeds_r")
#         for k, v in seeds_r.items():
#             print(f"{k}: {v}")
#             print(f"len : {v.stop - v.start}")
#             input()
#         seeds = list(set([num for _range in seeds_r.values() for num in _range]))
#         print("completed seeds")
#         # print(seeds)
#         for s in seeds:
#             n = s
#             # print(f"seed: {n}")
#             for k, v in mapping.items():
#                 # print(f"{orderd_map[k]}: {v}")
#                 for _range in v:
#                     if n in _range[1]:
#                         # print(f"{k}: {n} in {_range[1]}")
#                         # print(f"delta : {_range[3]}")
#                         n += _range[3]
#                         # print(f"{k}: new number is {n}")
#                         break
#             # input()
#             if n < result:
#                 result = n
