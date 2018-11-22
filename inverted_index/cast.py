from settings import ENCODING, INDEX_LENGTH
from v1 import v1
from v2 import v2
from v3 import v3
from v4 import v4
from v5 import v5

def v1row_to_v2row(v1row):
    return v2.kv_to_row(v1.row_to_kv(v1row))

def v2row_to_v3row(v1row, intbytes=2, index_length=INDEX_LENGTH):
    return v3.kv_to_row(v2.row_to_kv(v1row), intbytes=intbytes, index_length=index_length)

def v2row_to_vp4row(v1row, mp, intbytes=2, index_length=INDEX_LENGTH):
    return v4.kv_to_prow(v2.row_to_kv(v1row), mp, intbytes=intbytes, index_length=index_length)

def v2row_to_vp5row(v1row, mp, intbytes=2, index_length=INDEX_LENGTH):
    return v5.kv_to_prow(v2.row_to_kv(v1row), mp, intbytes=intbytes, index_length=index_length)

def v2row_to_v4row(v1row, intbytes=2, index_length=INDEX_LENGTH):
    return v4.kv_to_row(v2.row_to_kv(v1row), intbytes=intbytes, index_length=index_length)


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


def v2_to_v3(v2file, v3file, intbytes=3, index_length=INDEX_LENGTH):
    with open(v2file, "r", encoding=ENCODING) as rf:
        with open(v3file, "wb") as wf:
            wf.write(v3.int_to_bytes(intbytes, intbytes=2))
            wf.write(v3.int_to_bytes(index_length, intbytes=2))
            i = 0
            for l in rf.readlines():
                r = v2row_to_v3row(l, intbytes=intbytes, index_length=index_length)
                wf.write(r)
                print(i)
                i+=1

def v2_to_v4(v2file, v3file, intbytes=3, index_length=INDEX_LENGTH):
    with open(v2file, "r", encoding=ENCODING) as rf:
        with open(v3file, "wb") as wf:
            wf.write(v3.int_to_bytes(intbytes, intbytes=2))
            wf.write(v3.int_to_bytes(index_length, intbytes=2))
            i = 0
            for l in rf.readlines():
                r = v2row_to_v4row(l, intbytes=intbytes, index_length=index_length)
                wf.write(r)
                print(i)
                i+=1

def v2_to_vp4(v2file, v3file, urlmap, intbytes=3, index_length=INDEX_LENGTH):
    with open(urlmap, "r", encoding=ENCODING) as rf:
        mp = []
        for l in rf.readlines():
            splt = l.replace("\n", "").split("|")
            mp.append((int(splt[0]), int(splt[1])))
    mp = list(map(lambda x: x[0], sorted(mp, key=lambda x: x[1])))

    with open(v2file, "r", encoding=ENCODING) as rf:
        with open(v3file, "wb") as wf:
            wf.write(v3.int_to_bytes(intbytes, intbytes=2))
            wf.write(v3.int_to_bytes(index_length, intbytes=2))
            i = 0
            for l in rf.readlines():
                r = v2row_to_vp4row(l, mp, intbytes=intbytes, index_length=index_length)
                wf.write(r)
                print(i)
                i+=1

def v2_to_vp5(v2file, v5file, urlmap, intbytes=3, index_length=INDEX_LENGTH):
    with open(urlmap, "r", encoding=ENCODING) as rf:
        mp = []
        for l in rf.readlines():
            splt = l.replace("\n", "").split("|")
            mp.append((int(splt[0]), int(splt[1])))
    mp = list(map(lambda x: x[0], sorted(mp, key=lambda x: x[1])))

    with open(v2file, "r", encoding=ENCODING) as rf:
        with open(v5file, "wb") as wf:
            wf.write(v3.int_to_bytes(intbytes, intbytes=2))
            wf.write(v3.int_to_bytes(index_length, intbytes=2))
            i = 0
            for l in rf.readlines():
                r = v2row_to_vp5row(l, mp, intbytes=intbytes, index_length=index_length)
                wf.write(r)
                print(i)
                i+=1


# def v2row_to_v3row()