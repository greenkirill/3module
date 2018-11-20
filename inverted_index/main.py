from init_ii import *
from v1 import v1
from v2 import v2
from settings import INPUT_JSON_FILE_PATH
from utils import *
from time import time
if __name__ == '__main__':
    fll = "./out/spbu.ii2"
    fl = v2(fll, "./urls.url", loadf=True)
    inp = "1"
    res = []
    print(fll, "загружен")
    while inp != "":
        inp = input("Найти: ")
        res = fl.find_word(inp)
        print(len(res))
        for i in res:
            print(i)