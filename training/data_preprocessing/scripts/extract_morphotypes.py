#!/usr/bin/python3
import random
from PIL import Image, ImageDraw, ImageFont

with open("annotations/Ifremer_v2.csv") as f:
    lines = [l.rstrip("\n") for l in f.readlines()]

sponges = {}
for i,l in enumerate(lines):
    if i <= 0:
        continue

    params = l.split(";")

    specy = params[2]
    s = sponges.get(specy, [])

    annotation = {}
    annotation["category"] = params[2]
    annotation["filename"] = params[8]
    annotation["points"] = [float(p) for p in params[13][1:-1].split(",")]

    s.append(annotation)
    sponges[specy] = s

sponges = {k: v for k, v in reversed(sorted(sponges.items(), key=lambda item: len(item[1])))}

print("Categories found : ")
for n,c in sponges.items():
    print("[%s] : %d" % (n, len(c)))

print("Extracting samples...")
samples = {}
for n,c in sponges.items():
    cat_samples = random.sample(c, 16)
    samples[n] = cat_samples


for n,c in samples.items():
    print("Extracting %s... " % n, end="")

    img = Image.new("RGB", (685, 780), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    title = ImageFont.truetype("scripts/assets/calibri.ttf", 30)
    text = ImageFont.truetype("scripts/assets/calibri.ttf", 18)
    draw.text((30, 30), "Morphotype : %s (%d annotations)" % (n, len(sponges[n])), (0, 0, 0), title)

    annot_file = open("morphotypes/" + n + ".txt", "w")
    annot_file.write("Annotations %s\n\n" % n)

    for i,annot in enumerate(c):
        p = annot["points"]
        annot_file.write("%d : %s at (x: %d, y: %d)\n" % (i, annot["filename"], int(p[0]), int(p[1])))

        f = Image.open("/mnt/g/PL07/" + annot["filename"])
        region = f.crop((p[0] - 1.5*p[2], p[1] - 1.5*p[2], p[0] + 1.5*p[2], p[1] + 1.5*p[2]))
        region = region.resize((125, 125))

        img.paste(region, box=(40 + 160*(i%4), 80 + 175*(i//4)))
        draw.text((40 + 160*(i%4) + 58, 80 + 175*(i//4) + 135), str(i+1), (0, 0, 0), text, align="middle") 

    annot_file.close()

    img.save("morphotypes/" + n + ".png")

    print("Ok")
