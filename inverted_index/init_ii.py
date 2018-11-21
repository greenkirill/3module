from settings import INPUT_JSON_FILE_PATH, N_FILES, N_PROCESSES
from utils import *
import multiprocessing
from os import getpid
import time


def div_list(n, lst):
    N = len(lst)
    c = N // n
    ret = []
    for i in range(n - 1):
        ret.append(lst[c * i:c * (i + 1)])
    ret.append(lst[c * (n - 1):])
    return ret


def div2_list(n, lst):
    N = len(lst)
    c = N // n
    ret = []
    for i in range(c - 1):
        ret.append(lst[n * i:n * (i + 1)])
    ret.append(lst[n * (c - 1):])
    return ret


def div3_list(n, lst):
    N = len(lst)
    c = N // n
    ret = []
    for i in range(c - 1):
        ret.append((lst[n * i:n * (i + 1)], i))
    ret.append((lst[n * (c - 1):], c - 1))
    return ret


def foo(filelst):
    megalst = []
    itr = 0
    pid = getpid()
    for f in filelst:
        megalst += get_2list(f)
        # print("%i: %i megalst len %i" % (pid, itr, len(megalst)))
        itr += 1
    return megalst

# Каждый filelst в свой out_file
def foo3(filelst):
    megalst = []
    pid = getpid()
    print("%i" % pid)
    for f in filelst[0]:
        megalst += get_2list(f)
        # print("%i: %i megalst len %i" % (pid, itr, len(megalst)))
    save_to_v1file(megalst, "./out_%i.out" % filelst[1])
    print("%i megalst len %i" % (pid, len(megalst)))
    return 0

# Параллельный сбор данных
def step1():    
    start = time.time()
    # Список файлов
    filelist = get_filelist(INPUT_JSON_FILE_PATH)
    end1 = time.time()
    # Делим список по 1000
    newlst = div3_list(1000, filelist)
    end2 = time.time()
    # Берем пул из N процессов. лучше сколько ядер столько и процессов
    pool = multiprocessing.Pool(processes=N_PROCESSES)
    # Отдаем пулу наш список списков
    ret = pool.map(foo3, newlst)
    end3 = time.time()
    end = time.time()
    print(end1 - start, end2 - start, end3 - start, end - start)

# Вторым шагом собрать все out файлы в один большой
def step2():
    mega = []
    for i in range(69):
        mega += get_out_lines("./out_%i.out" % i)
        print(i, len(mega))
    save_to_v1file(mega, "./spbu.ii")
