#!/usr/bin/python3
from glob import glob
import random

RATIO_TRAINING = 95
RATIO_TEST = 5
RATIO_VALIDATION = 0

assert(RATIO_TRAINING + RATIO_TEST + RATIO_VALIDATION == 100)

files = set(glob("data/data/*.jpg"))
N = len(files)

training_set = random.sample(list(files), round(RATIO_TRAINING*N/100))

files = files.difference(set(training_set))

test_set = set([])
validation_set = set([])
if RATIO_VALIDATION == 0:
    test_set = files.copy()
else:
    test_set = random.sample(list(files), round(RATIO_TEST*N/100))
    files = files.difference(list(test_set))
    validation_set = files.copy()


with open("data/train.txt", "w") as o:
    for f in training_set:
        o.write(f + "\n")

with open("data/test.txt", "w") as o:
    for f in test_set:
        o.write(f + "\n")

if RATIO_VALIDATION > 0 :
    with open("data/validation.txt", "w") as o:
        for f in validation_set:
            o.write(f + "\n")

print("Results : ")
print("Total images : %d" % N)
print("Training set : %d images (%.1f%%)" % (len(training_set), RATIO_TRAINING))
print("Test set : %d images (%.1f%%)" % (len(test_set), RATIO_TEST))
print("Validation set : %d images (%.1f%%)" % (len(validation_set), RATIO_VALIDATION))
