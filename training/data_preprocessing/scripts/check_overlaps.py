#!/usr/bin/python3
from glob import glob
from datetime import datetime

files = list(set(glob("data/data/*.jpg")))
files.sort()

prevtime = None
assoc = {}

with open("data/test.txt") as f:
    test = [l.rstrip("\n") for l in f]
    test = [l.split("/")[-1] for l in test]

for i,f in enumerate(files):
    f = f.split("/")[-1]
    time = datetime(int(f[0:4]), int(f[4:6]), int(f[6:8]), int(f[9:11]), int(f[11:13]), int(f[13:15]))

    assoc[time] = f

timestamps = sorted(assoc.keys())

overlaps = []
for i,t in enumerate(timestamps):
    if i == 0:
        continue

    if (t-timestamps[i-1]).total_seconds() < 4:
        overlaps.append((timestamps[i-1], t))

test_overlaps = []
for o in overlaps:
    if assoc[o[0]] in test or assoc[o[1]] in test:
        test_overlaps.append("%s / %s" % (assoc[o[0]], assoc[o[1]]))

print("Total images : %d" % len(files))
print("Total overlaps : %d" % len(overlaps))
print("Test set overlaps : %d" % len(test_overlaps))
for o in test_overlaps:
    print(o)