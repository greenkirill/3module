from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import RussianStemmer
from settings import INPUT_TXT_FILES_DIR_PATH, INDEX_LENGTH, ENCODING
import json
import re

def get_out_lines(file):
    with open(file, "r", encoding=ENCODING) as fr:
        lines = fr.readlines()
    ret = []
    for l in lines:
        l = l.replace("\n", "")
        splt = l.split("|")
        ret.append((splt[0], l[len(splt[0])+1:]))
    return ret

def get_filelist(jsonfile):
    with open(jsonfile) as f:
        data = json.load(f)
    ret = []
    for i in range(len(data)):
        d = data[i]
        ret.append(("%s%s.txt" % (INPUT_TXT_FILES_DIR_PATH, d["f_n"]), d["url"], str(i)))
    return ret

def save_normallst(jsonfile, resfile):
    with open(jsonfile) as f:
        data = json.load(f)
    with open(resfile, "w") as wf:
        d = data[0]
        wf.write("%s" % d["url"])
        for i in range(1, len(data)):
            d = data[i]
            wf.write("\n%s" % d["url"])
        


def get_sorted_indexes(d):
    return sorted(d.keys())


def save_dict(d, file):
    with open(file, "w") as wf:
        for key in get_sorted_indexes(d):
            wf.write("%s,%s" % (key, ",".join(d[key])))


def stopwords_filter(words, lang="russian"):
    stopWords = set(stopwords.words(lang))
    return [w for w in words if w not in stopWords]


def get_words_from_file(file, lang="russian"):
    with open(file, "r", encoding=ENCODING) as rf:
        data = rf.read()
    return word_tokenize(data)


def onlyruwords_filter(words):
    regex = re.compile(r'^[а-яё]+$', re.I)
    return filter(regex.search, words)


def stem_russian_words(words):
    stemmer = RussianStemmer()
    return [stemmer.stem(w) for w in words]


def stem_words(words, lang="russian"):
    if lang == "russian":
        return stem_russian_words(words)
    return words


def get_2list(f, lang="russian"):
    words = get_words_from_file(f[0])
    words = onlyruwords_filter(words)
    words = stopwords_filter(words)
    words = stem_words(words)
    uniqwords = []
    for word in words:
        if word not in uniqwords and len(word) <= INDEX_LENGTH:
            uniqwords.append(word)
    return [(word, f[2]) for word in uniqwords]


def merge2lists(list1, list2):
    return list1 + list2

def save_to_file(lst, filename):
    lst = filter(lambda x: len(x[0]) <= INDEX_LENGTH, lst)
    srtd = sorted(lst, key=lambda x: x[0])
    with open(filename, "w", encoding=ENCODING) as wf:
        gen = srtd[0][0]
        wf.write("%s|%s" % (gen, srtd[0][1]))
        for i in range(1, len(srtd)):
            cur = srtd[i]
            if cur[0] == gen:
                wf.write("|%s" % cur[1])
            else:
                gen = cur[0]
                wf.write("\n%s|%s" % (gen, cur[1]))

# def save_to_v2file(lst, filename):
#     lst = filter(lambda x: len(x[0]) <= INDEX_LENGTH, lst)
#     srtd = sorted(lst, key=lambda x: x[0])
#     with open(filename, "w", encoding=ENCODING) as wf:
#         gen = srtd[0][0]
#         wf.write("{:{INDEX_LENGTH}s} {:s}".format(gen, srtd[0][1], INDEX_LENGTH=INDEX_LENGTH)
#         for i in range(1, len(srtd)):
#             cur = srtd[i]
#             if cur[0] == gen:
#                 wf.write("|{:s}".format(cur[1]))
#             else:
#                 gen = cur[0]
#                 wf.write("\n{:{INDEX_LENGTH}s} {:s}".format(gen, srtd[0][1], INDEX_LENGTH=INDEX_LENGTH)



