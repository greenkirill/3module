from init_ii import *
from v1 import v1
from v2 import v2
from v3 import v3
from settings import INPUT_JSON_FILE_PATH, INDEX_LENGTH
from utils import *
from time import time
from cast import *

from time import time
if __name__ == '__main__':
    v2_to_vp4("./iis/spbu.ii2", "./iis/spbup.ii4", "./inputs/urlmap.map")
    # v2_to_v4("./iis/spbu.ii2", "./iis/spbu.ii4")
    # fll3 = "C:\\Users\\kirill.gribkov\\Documents\\uni\\ggl\\inverted_index\\iis\\spbu.ii3"
    # fll2 = "C:\\Users\\kirill.gribkov\\Documents\\uni\\ggl\\inverted_index\\iis\\spbu.ii2"
    # fl3 = v3(fll3, "C:\\Users\\kirill.gribkov\\Documents\\uni\\ggl\\inverted_index\\inputs\\urls.url", loadf=True)
    # print(fll3, "загружен")
    # fl2 = v2(fll2, "C:\\Users\\kirill.gribkov\\Documents\\uni\\ggl\\inverted_index\\inputs\\urls.url", loadf=True)
    # print(fll2, "загружен")
    # inp = "1"
    # res = []
    # while inp != "":
    #     inp = input("Найти: ")
    #     start = time()
    #     res = fl3.find_word(inp)
    #     end = time()
    #     print("3", len(res), end-start)
    #     start = time()
    #     res = fl2.find_word(inp)
    #     end = time()
    #     print("2", len(res), end-start)
        # for i in res:
            # print(i)