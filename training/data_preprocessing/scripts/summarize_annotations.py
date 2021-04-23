#!/usr/bin/python3
from sys import argv

filename = "data.csv"

if len(argv) == 2:
    filename = argv[1].rstrip(".csv") + ".csv"

    with open(filename) as f:
        lines = [l.rstrip("\n") for l in f.readlines()]

        sponges = {}
        files = set([])
        for i,l in enumerate(lines):
            if i <= 0:
                continue

            params = l.split(";")

            specy = params[2]
            sponges[specy] = sponges.get(specy, 0) + 1
            files = files.union(set([params[8]]))

        for n,c in sponges.items():
            print("[%s] : %d" % (n, c))

        print("Images : %d" % len(files))
else:
    print("Missing argument")
    print("Usage : ")
    print("\tpython summarize_annotations.py [path_to_annotations_file]")