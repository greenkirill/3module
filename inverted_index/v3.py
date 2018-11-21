from settings import ENCODING, INDEX_LENGTH
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
import time


class v3:

    def __init__(self, filename, mp, loadf=True, encoding=ENCODING, lang="ru"):
        start = time.time()
        self.filename = filename
        self.lst = []
        self.isLoad = False
        self.mp = []
        self.load_mp(mp)
        start1 = time.time()
        if loadf:
            self.load_list_from_file()
        self.N = len(self.lst)
        start2 = time.time()
        print(start1 - start)
        print(start2 - start1)
        self.encoding=encoding

    def load_mp(self, fl):
        with open(fl, "r", encoding=ENCODING) as rf:
            self.mp = [l[:-1] for l in rf.readlines()]

    def load_list_from_file(self):
        with open(self.filename, "rb") as rf:
            intbytes = v3.bytes_to_int(rf.read(2))
            self.intbytes = intbytes
            index_length = v3.bytes_to_int(rf.read(2))
            wordbytes = v3.index_length(index_length=index_length)
            key = rf.read(wordbytes)
            while key != b'':
                for i in range(wordbytes-1, -1, -1):
                    if key[i] != 0:
                        key = key[:i+1]
                        break
                n = v3.bytes_to_int(rf.read(intbytes))
                self.lst.append((key, rf.read(n*intbytes)))
                key = rf.read(wordbytes)
    
    def map_url(self, i): return self.mp[i]
    
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
            f = 0
            t = self.intbytes
            n = len(self.lst[i][1])//self.intbytes
            for i in range(n):
                values.append(int.from_bytes(self.lst[i][1][f:t], byteorder="big"))
                t += self.intbytes
                f += self.intbytes
            return list(map(self.map_url, values)) 
        return []

    @staticmethod
    def kv_to_row(kv, lang="ru", encoding=ENCODING, intbytes=4, byteorder="big", index_length=INDEX_LENGTH):
        wordbytes = v3.index_length(
            lang=lang, encoding=encoding, index_length=index_length)
        rw = bytes(kv[0] + "\0", encoding=encoding)
        rw += bytes(bytearray(wordbytes-len(rw)))

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
        wordbytes = v3.index_length(
            lang=lang, encoding=encoding, index_length=index_length)
        key = row[:wordbytes]
        for i in range(wordbytes-1, -1, -1):
            if key[i] != 0:
                key = key[:i+1]
                break
        n = v3.bytes_to_int(
            row[wordbytes:wordbytes+intbytes], byteorder=byteorder)
        f = wordbytes+intbytes
        t = f+intbytes
        values = []
        for i in range(n):
            values.append(int.from_bytes(row[f:t], byteorder=byteorder))
            t += intbytes
            f += intbytes
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
