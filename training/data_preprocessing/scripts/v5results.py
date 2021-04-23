with open("v5results.txt") as f:
    lines = [l.rstrip("\n") for l in f]

with open("v5results.csv", "w") as f:
    for l in lines:
        s = l.split(" ")
        print(s)
        e = int(s[0].split("/")[0])
        if e%10 == 0:
            f.write("%s;%s\n" % (str(e), s[10]))