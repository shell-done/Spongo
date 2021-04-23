with open("maps.txt") as f:
    lines = [l.rstrip("\n") for l in f]
    
    maps = {}
    for l in lines:
        s = l.split()
        maps[s[1]] = s[7]

    nd = {}

    prev = None
    for k,v in maps.items():
        if v != prev:
            nd[k] = v
        prev = v

    print(nd)

    with open("o.csv", "w") as o:
        for k,v in nd.items():
            o.write("%s;%s\n" % (k, v))