from settings import ENCODING, INDEX_LENGTH
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
import time
from v3 import v3


class v4:

    def __init__(self, filename, mp, loadf=True, encoding=ENCODING, lang="ru"):
        pass

    @staticmethod
    def kv_to_row(kv, lang="ru", encoding=ENCODING, intbytes=4, byteorder="big", index_length=INDEX_LENGTH):
        wordbytes = v3.index_length(
            lang=lang, encoding=encoding, index_length=index_length)
        rw = bytes(kv[0], encoding=encoding)
        rw += bytes(bytearray(wordbytes-len(rw)))

        vls = b''

        s = ""
        for i in kv[1]:
            s += v4.int_to_edelta(i+1)
        N = len(s)//8
        vls += v4.int_to_bytes(N+1,
                               intbytes=intbytes, byteorder=byteorder)
        f = 0
        t = 8
        for i in range(N):
            vls += int(s[f:t], 2).to_bytes(1, "big")
            f += 8
            t += 8
        n = len(s) - N*8
        if n != 0:
            vls += int(s[f:t] + "0"*(8-n), 2).to_bytes(1, "big")
        return rw + vls

    @staticmethod
    def kv_to_prow(kv, mp, lang="ru", encoding=ENCODING, intbytes=4, byteorder="big", index_length=INDEX_LENGTH):
        
        wordbytes = v3.index_length(
            lang=lang, encoding=encoding, index_length=index_length)
        rw = bytes(kv[0], encoding=encoding)
        rw += bytes(bytearray(wordbytes-len(rw)))

        vls = b''

        s = ""
        for i in kv[1]:
            s += v4.int_to_edelta(mp[i]+1)
        N = len(s)//8
        vls += v4.int_to_bytes(N+1,
                               intbytes=intbytes, byteorder=byteorder)
        f = 0
        t = 8
        for i in range(N):
            vls += int(s[f:t], 2).to_bytes(1, "big")
            f += 8
            t += 8
        n = len(s) - N*8
        if n != 0:
            vls += int(s[f:t] + "0"*(8-n), 2).to_bytes(1, "big")
        return rw + vls

    @staticmethod
    def int_to_edelta(i):
        ln = 0
        lengthOfLen = 0
        temp = i
        res = ""
        while temp > 0:
            ln += 1
            temp >>= 1
        temp = ln
        while temp > 1:
            lengthOfLen += 1
            temp >>= 1
        res = "0" * (lengthOfLen)
        for j in range(lengthOfLen, -1, -1):
            res += str((ln >> j) & 1)
        for j in range(ln-2, -1, -1):
            res += str((i >> j) & 1)
        return res

    @staticmethod
    def int_to_bytes(i, intbytes=4, byteorder="big"):
        return (i).to_bytes(intbytes, byteorder=byteorder)

    @staticmethod
    def row_to_kv(row, lang="ru", encoding=ENCODING, intbytes=4, byteorder="big", index_length=INDEX_LENGTH):
        # wordbytes = v3.index_length(
        #     lang=lang, encoding=encoding, index_length=index_length)
        # key = row[:wordbytes]
        # for i in range(wordbytes-1, -1, -1):
        #     if key[i] != 0:
        #         key = key[:i+1]
        #         break
        # n = v3.bytes_to_int(
        #     row[wordbytes:wordbytes+intbytes], byteorder=byteorder)
        # f = wordbytes+intbytes
        # t = f+intbytes
        # values = []
        # for i in range(n):
        #     values.append(int.from_bytes(row[f:t], byteorder=byteorder))
        #     t += intbytes
        #     f += intbytes
        # return (key.decode(encoding), values)
        pass
