from settings import ENCODING

def v1row_to_v2row(v1row):
    i = 0
    while v1row[i] != "|":
        i += 1
    return "{:30s}{:s}".format(v1row[:i], v1row[i+1:-1])


def v1_to_v2(v1file, v2file):
    with open(v1file, "r", encoding=ENCODING) as rf:
        with open(v2file, "w", encoding=ENCODING) as wf:
            fl = True
            for l in rf.readlines():
                r = v1row_to_v2row(l)
                if 0 < len(r[0]) < 31:
                    if fl:
                        fl = False
                        wf.write("%s" % r)
                    else:
                        wf.write("\n%s" % r)


