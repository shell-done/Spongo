from glob import glob
import os
from shutil import copyfile
import random

files = list(glob("E:/Spongo/PL07/*.jpg"))
N = len(files)

print(N)
with open("../annotations/Ifremer_v4.csv") as f:
    lines = [l.rstrip("\n") for l in f.readlines()]

test_images = list([])
lines_set = list([])

files = [f.replace("\\", "/") for f in files]

for line in lines:
    lines_set.append(line.split(";")[8])

for line in set(lines_set):
    for file in files:
        if line == file.split("/")[-1]:
            test_images.append(file)

for image in set(test_images):
    os.remove(image)
    # copyfile(image, "D:/Utilisateurs/Margaux/Documents/Workspace/Projets_M1/Spongo_IHM/data/PL07_images/" + image.split("/")[-1])

print("Results : ")
print("Total images au départ : %d" % N)
print("Total images à l'arrivée : %d" % len(test_images))
