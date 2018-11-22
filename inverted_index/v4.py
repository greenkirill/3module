from settings import ENCODING, INDEX_LENGTH
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
import time
from v3 import v3
from bitarray import bitarray

class v4:

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
                values.append(v4.edelta_to_int(ba)-1)
            return list(map(self.map_url, values)) 
        return []

    @staticmethod
    def kv_to_prow(kv, mp, lang="ru", encoding=ENCODING, intbytes=4, byteorder="big", index_length=INDEX_LENGTH):
        rw = bytes(kv[0] + '\0', encoding=encoding)

        s = bitarray()
        for i in kv[1]:
            s += v4.int_to_edelta(mp[i]+1)
        s.fill()
        s.reverse()
        bts = s.tobytes()
        vls = v4.int_to_bytes(len(bts),
                               intbytes=intbytes, byteorder=byteorder) 

        return rw + vls + bts

    @staticmethod
    def kv_to_row(kv, lang="ru", encoding=ENCODING, intbytes=4, byteorder="big", index_length=INDEX_LENGTH):
        
        wordbytes = v3.index_length(
            lang=lang, encoding=encoding, index_length=index_length)
        rw = bytes(kv[0] + '\0', encoding=encoding)

        s = bitarray()
        for i in kv[1]:
            s += v4.int_to_edelta(i+1)
        s.fill()
        s.reverse()
        bts = s.tobytes()
        vls = v4.int_to_bytes(len(bts),
                               intbytes=intbytes, byteorder=byteorder) 

        return rw + vls + bts

    @staticmethod
    def int_to_edelta(i):
        ln = 0
        lengthOfLen = 0
        temp = i
        res = bitarray()
        while temp > 0:
            ln += 1
            temp >>= 1
        temp = ln
        while temp > 1:
            lengthOfLen += 1
            res.append(False)
            temp >>= 1
        for j in range(lengthOfLen, -1, -1):
            res.append((ln >> j) & 1)
        for j in range(ln-2, -1, -1):
            res.append((i >> j) & 1)
        return res

    @staticmethod
    def edelta_to_int(ba):
        num = 1
        ln = 1
        lengthOfLen = 0
        while not ba.pop():   
            lengthOfLen+= 1
        for i in range(lengthOfLen):
            ln <<= 1
            ln |= ba.pop()
        for i in range(ln-1):
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
            values.append(v4.edelta_to_int(ba)-1)
        return (key.decode(encoding), values)
