import csv
import pathlib
import urlparse


count_pages = 0
count_not_found = 0
count_links = 0
count_links_inner = 0
count_links_outer = 0
count_src = 0
count_sub = 0

dict_types = {}
dict_domens = {}

subs = []

outcount = 0

for row in csv.reader( open('apmath.csv', 'r') ):
    try:

        if row[0]=="0" and (row[3] == "403" or row[3]== "404"):
            count_not_found += 1

        if row[0]=="0":
            count_pages+=1
            sb = row[1].split("://")[1].split('/')[0]
            if not(sb in subs):
                count_sub += 1
                subs.append(sb)
            extension = pathlib.Path(row[1]).suffix[0:5]
            if dict_types.get(extension) == None:
                dict_types[extension] = 1
            else:
                dict_types[extension] = dict_types.get(extension) + 1

        if row[0] == "1":
            count_links += 1
            domen = urlparse.urlparse(row[2]).hostname
            # if outcount < 10:
            #     print domen
            if domen[-14:] == "apmath.spbu.ru":
                count_links_inner += 1
            else:
                count_links_outer += 1

            if dict_domens.get(domen) == None:
                dict_domens[domen] = 1
            else:
                dict_domens[domen] = dict_domens.get(domen) + 1

        if row[0] == "2":
            print "src"
            count_src += 1

        outcount += 1
    except Exception:
        print "illegal row: ", row
# for k , v in dict_domens.iteritems():
#         print k+"\t", v

print(subs)
print("Found '': ", dict_types.get(""))
print("Found htm%: ", dict_types.get(".htm%"))
print("Found htm: ", dict_types.get(".htm"))
print("Found html: ", dict_types.get(".html"))
print("Found php?: ", dict_types.get(".php?"))



print("Found pages: ", count_pages)
print("Not found: ", count_not_found)
print("Count links: ", count_links)
print("Count sub: ", count_sub)

print("Count inner links: ", count_links_inner)
print("Count outter links: ", count_links_outer)

print("Count src links: ", count_src)
print("Count pdf: ", dict_types.get(".pdf"))
print("Count doc: ", dict_types.get(".doc"))
print("Count docx: ", dict_types.get(".docx"))