from settings import ENCODING, INDEX_LENGTH
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
import time

class v2:

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
            self.lst = [self.read_row(l) for l in rf.readlines()]
            self.isLoad = True
            self.N = len(self.lst)

    def map_url(self, i): return self.mp[int(i)]

    def read_v1_row(self, row):
        values = row.split("|")
        values[-1] = values[-1][:-1]
        key = values.pop(0)
        return (key, list(map(self.map_url, values)))

    def read_row(self, s):
        return (str.strip(s[:30]), s[30:])


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