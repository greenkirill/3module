from random import randint

# N = 100

# intlist = []
# for i in range(N):
#     intlist.append(randint(0,1000000))

# IN1 = 30
# IN2 = 10

# word = "достопримечательность"


# s1 = ""
# s1 += "{:30s}".format(word)
# for i in intlist:
#     s1+= "{:>10d}".format(i)

# s2 = "{:30s}".format(word)
# s2 += "|".join(map(str, intlist))

# with open("t1.txt", "w", encoding="utf-8") as wf:
#     wf.write(s1)
# with open("t2.txt", "w", encoding="utf-8") as wf:
#     wf.write(s2)

s1 = "достопримечательность             893693    464699    433528    271430    127604     34701    757746    418846    805256    590043    373400    746557    195512    938731     74928     64153    280460    890356    759794    651252    914720    867633    753980    827417    729411    809904    403485    650621    871906    598410    656918    732418    927235      2112    294217     47006    978136    525316    529707    322652    933660    713390    543896    641718    446099    158802     66044    501775    375195     53861    289259    916731    832224    197804    295353    886219    174546    718149    974263    601989    495549    866998    866648    666086    396949    547289    753792    902604    590620    660966     25807    591146    351578    290373    406670    626982    602597    322991    771926    294323    932649    911844    247198    652987    864777    448272    810910    446740    839217    678416    697657    872714    695027    798606    891665    249007    183186    375794    632777    904316"
s2 = "достопримечательность         893693|464699|433528|271430|127604|34701|757746|418846|805256|590043|373400|746557|195512|938731|74928|64153|280460|890356|759794|651252|914720|867633|753980|827417|729411|809904|403485|650621|871906|598410|656918|732418|927235|2112|294217|47006|978136|525316|529707|322652|933660|713390|543896|641718|446099|158802|66044|501775|375195|53861|289259|916731|832224|197804|295353|886219|174546|718149|974263|601989|495549|866998|866648|666086|396949|547289|753792|902604|590620|660966|25807|591146|351578|290373|406670|626982|602597|322991|771926|294323|932649|911844|247198|652987|864777|448272|810910|446740|839217|678416|697657|872714|695027|798606|891665|249007|183186|375794|632777|904316"
s3 = "достопримечательность|893693|464699|433528|271430|127604|34701|757746|418846|805256|590043|373400|746557|195512|938731|74928|64153|280460|890356|759794|651252|914720|867633|753980|827417|729411|809904|403485|650621|871906|598410|656918|732418|927235|2112|294217|47006|978136|525316|529707|322652|933660|713390|543896|641718|446099|158802|66044|501775|375195|53861|289259|916731|832224|197804|295353|886219|174546|718149|974263|601989|495549|866998|866648|666086|396949|547289|753792|902604|590620|660966|25807|591146|351578|290373|406670|626982|602597|322991|771926|294323|932649|911844|247198|652987|864777|448272|810910|446740|839217|678416|697657|872714|695027|798606|891665|249007|183186|375794|632777|904316"


# def foo1(s: str):
#     key = str.strip(s[:30])
#     values = []
#     N = len(s[30:]) // 10
#     f = 30
#     t = 40
#     for i in range(N):
#         values.append(int(str.strip(s[f:t])))
#         t += 10
#         f += 10

def foo2(s:str):
    key = str.strip(s[:30])
    values = s[30:]
    

def foo3(s:str):
    values = s.split("|")
    key = values.pop(0)
    values = list(map(int, values))

def foo4(s:str):
    values = s.split("|")
    key = values.pop(0)
    values = s[len(key):]

def foo5(s:str):
    i = 0
    while s[i] != "|":
        i += 1
    key = s[:i]
    values = s[i+1:]


import timeit
# print(timeit.timeit('foo1(s1)', globals=globals(), number=10000))
print(timeit.timeit('foo2(s2)', globals=globals(), number=100000))
# print(timeit.timeit('foo3(s3)', globals=globals(), number=10000))
# print(timeit.timeit('foo4(s3)', globals=globals(), number=10000))
print(timeit.timeit('foo5(s3)', globals=globals(), number=100000))


# with open("./out/spbu.ii2", "rb") as rf: 
#     byte = rf.read(1)
#     dct = {}
#     while byte != b"":
#         i = int.from_bytes(byte, byteorder='little')
#         if i in dct:
#             dct[i] += 1
#         else:
#             dct[i] = 1
#         byte = rf.read(1)
#     lst = [(l, dct[l]) for l in dct]


# b = bytes("ёёёёёёёёёёёёёёёёёёёёёёёёёёёёёё", "KOI8-R")
# print(b)
# print(len(b))
# print(b.encode("KOI8-R"))

# from v3 import v3

# def fff():
#     a = ("абв", [1,2,3])
#     b = v3.kv_to_row(a)
#     # c = v3.row_to_kv(b)



# print(timeit.timeit('fff()', globals=globals(), number=100000))
s = b'asdddjoiqwjd\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x01'

# with open("./inputs/test33.txt", "wb") as wf:
#     wf.write(s)
# def fb1():
#     with open("./inputs/test33.txt", "rb") as rf:
#         b = b""
#         rb = rf.read(1)
#         while rb != b"\x00":
#             b += rb
#             rb = rf.read(1)
#         rf.read(59-len(b))

# def fb2():
#     with open("./inputs/test33.txt", "rb") as rf:
#         b = rf.read(60)
#         for i in range(60):
#             if b[i] == 0:
#                 b = b[:i]
#                 break

# def fb3():
#     with open("./inputs/test33.txt", "rb") as rf:
#         b = rf.read(60)
#         for i in range(59, -1, -1):
#             if b[i] != 0:
#                 b = b[:i+1]
#                 break


# print(timeit.timeit('fb1()', globals=globals(), number=10000))
# print(timeit.timeit('fb2()', globals=globals(), number=10000))
# print(timeit.timeit('fb3()', globals=globals(), number=10000))
