from settings import ENCODING, INDEX_LENGTH
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
from time import time
from v3 import v3
from bitarray import bitarray
from v2 import kv_to_k2v

class v5:

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
            rf.read(2)
            key = b''
            k = rf.read(1)
            while k != b'' and k != b'\x00':
                key += k
                k = rf.read(1)
            while key != b'':
                n = v3.bytes_to_int(rf.read(intbytes))
                self.lst.append((key, rf.read(n)))
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
        i=t

        if bw == self.lst[i][0]:
            values = []
            ba = bitarray()
            ba.frombytes(self.lst[i][1])
            while ba.any():
                values.append(v5.egamma_to_int(ba)-1)
            kv = (word, values)
            return list(map(self.map2_url, kv_to_k2v(kv)[1]))
            # return list(map(self.map_url, values)) 
        return []

    def find_print_word(self, word, tme=True, tp=False):
        start = time()
        res = self.find_word(word)
        end = time()
        if tme:
            print("\n\nГамма Элиас, количество страниц:", len(res), "\n Поиск и парсинг", end-start)
        if tp:
            for l in sorted(res, key=lambda x:-x[1])[:10]:
                print(l[1], l[0])

    @staticmethod
    def kv_to_prow(kv, mp, lang="ru", encoding=ENCODING, intbytes=4, byteorder="big", index_length=INDEX_LENGTH):
        rw = bytes(kv[0] + '\0', encoding=encoding)

        s = bitarray()
        for i in kv[1]:
            s += v5.int_to_egamma(mp[i]+1)
        s.fill()
        s.reverse()
        bts = s.tobytes()
        vls = v5.int_to_bytes(len(bts),
                               intbytes=intbytes, byteorder=byteorder) 

        return rw + vls + bts

    @staticmethod
    def kv_to_row(kv, lang="ru", encoding=ENCODING, intbytes=4, byteorder="big", index_length=INDEX_LENGTH):
        rw = bytes(kv[0] + '\0', encoding=encoding)

        s = bitarray()
        for i in kv[1]:
            s += v5.int_to_egamma(i+1)
        s.fill()
        s.reverse()
        bts = s.tobytes()
        vls = v5.int_to_bytes(len(bts),
                               intbytes=intbytes, byteorder=byteorder) 

        return rw + vls + bts

    @staticmethod
    def int_to_egamma(i):
        ln = 0
        temp = i
        res = bitarray()
        while temp > 0:
            ln += 1
            temp >>= 1
        for j in range(ln-1):
            res.append(False)
        for j in range(ln-1, -1, -1):
            res.append((i >> j) & 1)
        return res

    @staticmethod
    def egamma_to_int(ba):
        num = 1
        ln = 0
        while not ba.pop():   
            ln+= 1
        for i in range(ln):
            num <<= 1
            num |= ba.pop()
        return num

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
        
        values = []
        ba = bitarray()
        ba.frombytes(row[wordbytes+intbytes:])
        while ba.any():
            values.append(v5.egamma_to_int(ba)-1)
        return (key.decode(encoding), values)
