from settings import ENCODING, INDEX_LENGTH
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
import time

class v1:

    def __init__(self, filename, mp, loadf=True):
        start = time.time()
        self.filename = filename
        self.lst = []
        self.isLoad = False
        self.mp = []
        self.load_mp(mp)
        start1 = time.time()
        if loadf:
            self.load_list_from_file()
        start2= time.time()
        print(start1 - start)
        print(start2 - start1)

    def load_mp(self, fl):
        with open(fl, "r", encoding=ENCODING) as rf:
            self.mp = [l[:-1] for l in rf.readlines()]

    def load_list_from_file(self):
        with open(self.filename, "r", encoding=ENCODING) as rf:
            start1= time.time()
            self.lst = [self.read_row(l) for l in rf.readlines()]
            start2= time.time()
            print(start2 - start1)
            self.isLoad = True
            self.N = len(self.lst)

    def map_url(self, i): return self.mp[int(i)]

    def read_v1_row(self, row):
        values = row.split("|")
        values[-1] = values[-1][:-1]
        key = values.pop(0)
        return (key, list(map(self.map_url, values)))

    def read_row(self, row):
        i = 0
        while row[i] != "|":
            i += 1
        return (row[:i], row[i+1:-1])

    @staticmethod
    def row_to_kv(v1row): 
        i = 0
        while v1row[i] != "|":
            i += 1
        return (v1row[:i], list(map(int, v1row[i+1:-1].split("|"))))

    @staticmethod
    def kv_to_row(kv): 
        return "{:s}|{:s}".format(kv[0], "|".join(kv[1]))

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
        return list(map(self.map_url, self.lst[t][1].split("|"))) if word == self.lst[t][0] else []
