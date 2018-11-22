from init_ii import *
from v1 import v1
from v2 import v2
from v3 import v3
from v4 import v4
from v5 import v5
from settings import INPUT_JSON_FILE_PATH, INDEX_LENGTH
from utils import *
from time import time
from cast import *

file_iis2 = "C:\\PROJECTS\\py\\ggl\\inverted_index\\iis\\spbush.ii2"
file_iis3 = "C:\\PROJECTS\\py\\ggl\\inverted_index\\iis\\spbu.ii3"
file_iis4 = "C:\\PROJECTS\\py\\ggl\\inverted_index\\iis\\spbu.ii4"
file_iis5 = "C:\\PROJECTS\\py\\ggl\\inverted_index\\iis\\spbu.iish5"
urlfile = "C:\\PROJECTS\\py\\ggl\\inverted_index\\inputs\\urls.url"
urlmapfile = "C:\\PROJECTS\\py\\ggl\\inverted_index\\inputs\\urlmap.map"

from time import time
if __name__ == '__main__':
    # fl3 = v3(file_iis3, urlfile, loadf=True)
    # print(file_iis3, "загружен")
    # fl2 = v2(file_iis2, "C:\\PROJECTS\\py\\ggl\\inverted_index\\inputs\\urls.url", loadf=True)
    # print(file_iis2, "загружен")
    fl5 = v5(file_iis5, urlfile, loadf=True)
    print(file_iis5, "загружен")
    inp = "1"
    res = []
    while inp != "":
        inp = input("Найти: ")
        start = time()
        res = fl5.find_word(inp)
        end = time()
        print("5", len(res), end-start)
        # for i in res:
            # print(i)
    pass