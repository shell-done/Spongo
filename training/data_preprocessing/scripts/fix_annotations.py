from glob import glob

filenames = glob("data/data/to_process/*.txt")
#filenames = ["data/data/to_process/20190917T073048.504178Z.txt"]

IMG_W = 4243
IMG_H = 2828

error_img = 0
empty_annot = 0
outside_annot = 0

for name in filenames:
    lines = open(name).readlines()
    lines = [l.rstrip("\n") for l in lines]

    out_name = name.replace("data/data/to_process/", "data/data/")

    with open(out_name, "w") as f:
        err = False
        for i,l in enumerate(lines):
            id, x, y, w, h = [float(n) for n in l.split(" ")]
            id = int(id)

            nx = x
            ny = y
            nw = w
            nh = h

            nl = l = x-w/2
            nr = r = x+w/2
            nt = t = y-h/2
            nb = b = y+h/2

            if nl <= 0: nl = 0.00001
            if nr >= 1: nr = 0.99999
            if nt <= 0: nt = 0.00001
            if nb >= 1: nb = 0.99999

            x_prob, y_prob = (False, False)
            if nl != l or nr != r:
                nx = (nl+nr)/2
                nw = nr-nl
                x_prob = True

            if nt != t or nb != b:
                ny = (nt+nb)/2
                nh = nb-nt
                y_prob = True

            if (r-l)*(b-t) <= 0:
                print("Zero or negative area on %s:%d" % (name, i))
                empty_annot += 1
                err = True
                continue

            if x_prob or y_prob:
                print("Annotation not fully inside the frame (x_axis: %d, y_axis: %d) on %s:%d" % (x_prob, y_prob, name, i))
                err = True
                outside_annot += 1

            f.write("%d %.6f %.6f %.6f %.6f\n" % (id, nx, ny, nw, nh))
        
        if err:
            error_img += 1

print("Operation completed on %d images" % len(filenames))
print("%d zero or negative area found (removed)" % empty_annot)
print("%d annotations (on %d images) not fully inside the frame found (fixed)" % (outside_annot, error_img))