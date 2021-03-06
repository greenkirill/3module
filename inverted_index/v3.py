from settings import ENCODING, INDEX_LENGTH
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
from time import time
import sys
from v2 import kv_to_k2v

class v3:

    def __init__(self, filename, mp, loadf=True, encoding=ENCODING, lang="ru"):
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
        self.N = len(self.lst)
        start2 = time()
        print("Загрузка map файла:", start1 - start)
        print("Загрузка файла обратного индекса:", start2 - start1)
        self.encoding=encoding
        print(filename, "загружен")

    def load_mp(self, fl):
        with open(fl, "r", encoding=ENCODING) as rf:
            self.mp = [l[:-1] for l in rf.readlines()]

    def load_list_from_file(self):
        with open(self.filename, "rb") as rf:
            intbytes = v3.bytes_to_int(rf.read(2))
            self.intbytes = intbytes
            index_length = v3.bytes_to_int(rf.read(2))
            wordbytes = v3.index_length(index_length=index_length)
            key = b''
            k = rf.read(1)
            while k != b'' and k != b'\x00':
                key += k
                k = rf.read(1)
            while key != b'':
                n = v3.bytes_to_int(rf.read(intbytes))
                self.lst.append((key, rf.read(n*intbytes)))
                key = b''
                k = rf.read(1)
                while k != b'' and k != b'\x00':
                    key += k
                    k = rf.read(1)
    
    def map_url(self, i): return self.mp[i]
    def map2_url(self, i): return (self.mp[int(i[0])], i[1])
    
    def find_word(self, word):
        stemmer = RussianStemmer()
        word = stemmer.stem(word)
        bw = bytes(word, encoding=self.encoding)
        f = 0
        t = self.N - 1
        while f != t:
            N = t - f + 1
            i = f + N // 2 
            if self.lst[i][0] > bw:
                t = i - 1
            else:
                f = i
            # print(N, i, f,t)
        values = []
        j=t
        if bw == self.lst[j][0]:
            f = 0
            t = self.intbytes
            n = len(self.lst[j][1])//self.intbytes
            for i in range(n):
                values.append(int.from_bytes(self.lst[j][1][f:t], byteorder="big"))
                t += self.intbytes
                f += self.intbytes
            kv = (word, values)
            return list(map(self.map2_url, kv_to_k2v(kv)[1]))
            # return list(map(self.map_url, values)) 
        return []
        
    def find_print_word(self, word, tme=True, tp=False):
        start = time()
        res = self.find_word(word)
        end = time()
        if tme:
            print("\n\nБайтфайл, количество страниц:", len(res), "\n Поиск и парсинг", end-start)
        if tp:
            for l in sorted(res, key=lambda x:-x[1])[:10]:
                print(l[1], l[0])

    @staticmethod
    def kv_to_row(kv, lang="ru", encoding=ENCODING, intbytes=4, byteorder="big", index_length=INDEX_LENGTH):
        rw = bytes(kv[0] + "\0", encoding=encoding)
        # rw += bytes(bytearray(wordbytes-len(rw)))

        vls = b''
        vls += v3.int_to_bytes(len(kv[1]),
                               intbytes=intbytes, byteorder=byteorder)
        for v in kv[1]:
            vls += v3.int_to_bytes(v, intbytes=intbytes, byteorder=byteorder)
        return rw + vls

    @staticmethod
    def int_to_bytes(i, intbytes=4, byteorder="big"):
        return (i).to_bytes(intbytes, byteorder=byteorder)

    @staticmethod
    def row_to_kv(row, lang="ru", encoding=ENCODING, intbytes=4, byteorder="big", index_length=INDEX_LENGTH):
        wb = 0
        b = row[wb]
        while b != 0:
            wb += 1
            b = row[wb]
        wordbytes = wb+1
        key = row[:wb]
        n = v3.bytes_to_int(
            row[wordbytes:wordbytes+intbytes], byteorder=byteorder)
        f = wordbytes+intbytes
        t = f+intbytes
        values = []
        sys.stdout.write("   ")
        for i in range(n):
            values.append(int.from_bytes(row[f:t], byteorder=byteorder))
            t += intbytes
            f += intbytes
            perc = (i*100)//n + 1
            sys.stdout.write("\b\b\b"+str.format("{1:3n}", perc))
            sys.stdout.flush()

        return (key.decode(encoding), values)

    @staticmethod
    def bytes_to_int(bts, byteorder="big"):
        return int.from_bytes(bts, byteorder=byteorder)

    @staticmethod
    def index_length(lang="ru", encoding=ENCODING, index_length=INDEX_LENGTH):
        ch = ""
        if lang == "ru":
            ch = "ё"
        elif lang == "en":
            ch = "a"
        s = ch * index_length
        b = bytes(s, encoding=encoding)
        return len(b)
