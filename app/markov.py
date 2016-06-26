#!/usr/bin/env python
import copy
import random
import sys

def weighted_choice(choices):
    total_weight = sum(choices.values())
    choice = random.randint(0, total_weight - 1)
    rkeys = sorted(choices.keys())

    while len(rkeys) > 0:
        k = rkeys.pop(0)
        if choices[k] > choice:
            return k
        choice -= choices[k]

allnames = []

for fn in sys.argv[1:]:
    names = []
    with open(sys.argv[1]) as fh:
        for line in fh:
            names.append(line.rstrip().lower())

    namelengths = {}
    sequences = { 1: {} }

    for name in names:
        namelengths[len(name)] = namelengths.get(len(name), 0) + 1
        sequences[1][name[0]] = sequences[1].get(name[0], 0) + 1

        for count in range(2, len(name)-1):
            if not count in sequences:
                sequences[count] = {}

            for i in range(len(name) - count + 1):
                start = name[i:i+count-1]
                end = name[i+count-1:i+count]
                if not start in sequences[count]:
                    sequences[count][start] = {}

                sequences[count][start][end] = sequences[count][start].get(end, 0) + 1

            name_end = name[1-count:]
            if not name_end in sequences[count]:
                sequences[count][name_end] = {}
            sequences[count][name_end][None] = sequences[count][name_end].get(None, 0) + 1

    gen_name = weighted_choice(sequences[1])
    while True:
        letters = copy.copy(sequences[2].get(gen_name[-1], {}))

        for count in range(3, len(gen_name)+2):
            if count in sequences and gen_name[1-count:] in sequences[count]:
                for k, v in sequences[count][gen_name[1-count:]].items():
                    letters[k] = letters.get(k, 0) + v * 2**(count-1)

        if len(gen_name) < min(namelengths.keys()):
            if None in letters:
                del letters[None]
        else:
            letters[None] = letters.get(None, 0) * len(names) / (1+sum([namelengths[n] for n in namelengths if n > len(gen_name)]))

        print "{:15} {}".format(gen_name.upper(), " ".join(["({} {:2d})".format("." if k is None else k, letters[k]) for k in sorted(letters.keys(), key=lambda x: letters[x], reverse=True)]))

        next_letter = weighted_choice(letters)
        if next_letter is None:
            break

        gen_name += next_letter

    allnames.append(gen_name.title())

print " ".join(allnames)

