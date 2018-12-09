# from init_ii import *
from v1 import v1
from v2 import v2
from v3 import v3
from v4 import v4
from v5 import v5
from settings import INPUT_JSON_FILE_PATH, INDEX_LENGTH, INPUT_URLS
from utils import *
from time import time
from cast import *

prefix_iis = "C:\\Users\\kirill.gribkov\\Documents\\uni\\ggl\\inverted_index\\iis\\"
prefix_inputs = "C:\\Users\\kirill.gribkov\\Documents\\uni\\3module\\inverted_index\\inputs\\"

file_iis1 =  prefix_iis + "spbu.ii"
file_iis2 =  prefix_iis + "spbu.ii2"
file_iis2_sh =  prefix_iis + "spbu_sh.ii2"
file_iis3 =  prefix_iis + "spbu.byteii"
file_iis3_sh =  prefix_iis + "spbu_sh.byteii"
file_iis4 =  prefix_iis + "spbu.ii4"
file_iis4_sh =  prefix_iis + "spbu_sh.ii4"
file_iis5 =  prefix_iis + "spbu.ii5"
file_iis5_sh =  prefix_iis + "spbu_sh.ii5"
urlfile =    prefix_inputs + "urls.url"
urlmapfile = prefix_inputs + "urlmap.map"

from time import time
if __name__ == '__main__':
    fl2 = v2(file_iis2, INPUT_URLS, loadf=True)
    fl3 = v3(file_iis3, INPUT_URLS, loadf=True)
    fl4 = v4(file_iis4, INPUT_URLS, loadf=True)
    fl5 = v5(file_iis5, INPUT_URLS, loadf=True)
    inp = "1"
    while inp != "":
        inp = input("Найти: ")
        fl2.find_print_word(inp, tp=True)
        fl3.find_print_word(inp, tp=True)
        fl4.find_print_word(inp, tp=True)
        fl5.find_print_word(inp, tp=True)
    pass