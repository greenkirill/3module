from settings import ENCODING, INDEX_LENGTH
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
from time import time


def kv_to_k2v(kv):
    v2 = list(zip(kv[1][::2], kv[1][1::2]))
    s = 0
    v2n = []
    for i in range(len(v2)):
        v2n.append((v2[i][0] + s, v2[i][1]))
        s = v2n[i][0]
    return (kv[0], v2n)

class v2:

    def __init__(self, filename, mp, loadf=True):
        print(filename, "начало загрузки")
        start = time()
        self.filename = filename
        self.lst = []
        self.isLoad = False
        self.mp = []
        self.load_mp(mp)
        start1 = time()
        if loadf:
            self.load_list_from_file()
        start2= time()
        print("Загрузка map файла:", start1 - start)
        print("Загрузка файла обратного индекса:", start2 - start1)
        print(filename, "загружен")

    def load_mp(self, fl):
        with open(fl, "r", encoding=ENCODING) as rf:
            self.mp = [l[:-1] for l in rf.readlines()]

    def load_list_from_file(self):
        with open(self.filename, "r", encoding=ENCODING) as rf:
            self.lst = [self.read_row(l) for l in rf.readlines()]
            self.isLoad = True
            self.N = len(self.lst)

    def map_url(self, i): return self.mp[int(i)]
    def map2_url(self, i): return (self.mp[int(i[0])], i[1])

    def read_v1_row(self, row):
        values = row.split("|")
        values[-1] = values[-1][:-1]
        key = values.pop(0)
        return (key, list(map(self.map_url, values)))

    def read_row(self, s):
        return (str.strip(s[:30]), s[30:])

    @staticmethod
    def row_to_kv(v1row): 
        
        return (str.strip(v1row[:30]), list(map(int, v1row[30:].split("|"))))

    @staticmethod
    def kv_to_row(kv): 
        return "{:30s}{:s}".format(kv[0], "|".join(map(str, kv[1])))

    def read_v1_row2(self, row):
        values = row.split("|")
        values[-1] = values[-1][:-1]
        key = values.pop(0)
        return (key, map(self.map_url, values))

    def find_word(self, word):
        stemmer = RussianStemmer()
        word = stemmer.stem(word)
        f = 0
        t = self.N - 1
        while f != t:
            N = t - f + 1
            i = f + N // 2 
            if self.lst[i][0] > word:
                t = i - 1
            else:
                f = i
            # print(N, i, f,t)
        if word == self.lst[t][0]:
            cur = self.lst[t]
            kv = (word, list(map(int, cur[1].split("|"))))
            return list(map(self.map2_url, kv_to_k2v(kv)[1]))
        else:
            return []

    def find_print_word(self, word, tme=True, tp=False):
        start = time()
        res = self.find_word(word)
        end = time()
        if tme:
            print("\n\nСтроковый файл, количество страниц:", len(res), "\n Поиск и парсинг", end-start)
        if tp:
            for l in sorted(res, key=lambda x:-x[1])[:10]:
                print(l[1], l[0])



        # return  if word == self.lst[t][0] else []