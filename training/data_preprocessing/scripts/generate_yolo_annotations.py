#!/usr/bin/python3
from os import path
from shutil import copyfile
from progress.bar import Bar

EXTRACT_IMAGES = True
EXTRACT_DATA = True
ANNOT_SIZE_COEFF = 2

categories = ["Ball", "Vase", "Corona", "Red", "Crown", "Grey_white"]

with open("annotations/Ifremer_v4.csv") as f:
    lines = [l.rstrip("\n") for l in f.readlines()]

    progress = Bar('Generating Yolo\'s annotations', max=len(lines))
    for i,l in enumerate(lines):
        progress.next()
        if i == 0:
            continue

        params = l.split(";")

        if params[2] in categories:
            if EXTRACT_IMAGES:
                if not path.exists("data/data/" + params[8]):
                    copyfile("/mnt/g/PL07/" + params[8], "data/data/" + params[8])

            if EXTRACT_DATA:
                o = open("data/data/" + params[8].rstrip(".jpg") + ".txt", "a")
                points = params[13][1:-1].split(",")
                points = [float(p) for p in points]

                attr = params[14][2:-2].split(",")
                img_width = int(attr[2].split(":")[1])
                img_height = int(attr[3].split(":")[1])

                class_id = categories.index(params[2])
                x_center, y_center = points[0], points[1]
                width = height = points[2]*ANNOT_SIZE_COEFF

                if x_center/img_width >= 1 or y_center/img_height >= 1:
                    print("Anormal annotation in %s" % params[8].rstrip(".jpg") + ".txt")

                o.write("%d %.6f %.6f %.6f %.6f\n" % (class_id, x_center/img_width, y_center/img_height, width/img_width, height/img_height))
                
                o.close()

    if EXTRACT_DATA:
        o = open("data/classes.names", "w")
        for c in categories:
            o.write(c + "\n")
        o.close()

    progress.finish()
