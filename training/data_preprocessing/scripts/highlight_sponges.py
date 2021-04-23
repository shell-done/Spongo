#!/usr/bin/python3
from PIL import Image, ImageDraw
from glob import glob
from progress.bar import Bar

categories = ["Ball", "Vase", "Corona", "Red", "Crown", "Grey_white"]
colors = ["lime", "white", "orange", "red", "cyan", "pink"]

files = set(glob("data/test/*.jpg"))

#with open("data/test.txt") as f:
#    files = [l.rstrip("\n") for l in f]

print(files)
#files = [l.replace("data/data", "pre_data") for l in files]

progress = Bar('Processing', max=len(files))
for f in files:
    progress.next()
    source = Image.open(f)
    draw = ImageDraw.Draw(source)

    img_width, img_height = source.size

    data = open(f.replace(".jpg", ".txt"))
    for d in data:
        params = d.split(" ")
        params = [float(p) for p in params]
        params[0] = int(params[0])

        color = colors[params[0]]
        x_center = int(params[1]*img_width)
        y_center = int(params[2]*img_height)
        
        width = int(params[3]*img_width)
        height = int(params[4]*img_height)

        tl = (x_center - width//2, y_center - height//2)
        br = (x_center + width//2, y_center + height//2)

        draw.rectangle((tl, br), fill=None, outline=color, width=10)

    source.save(f.replace("data/test", "data/test/highlighted"), "JPEG")

progress.finish()