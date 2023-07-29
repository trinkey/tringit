import json
import os

directory = os.path.abspath(".")
unnamedIndex = 1
unnamed = 1
try:
    f = json.loads(open("library.json", "r", encoding="utf-8").read().replace("\r\n", "\n"))
except:
    print("library.json not found! Run tringit and type 4 to create it.")
    exit()

def makeFile(path, contents, e=True):
    global directory
    try:
        f = open(f"{directory}/{path}", "w")
    except:
        f = open(f"{directory}/{path}", "x")
    if e:
        print(f"{directory}/{path}")
        print(contents)
        f.write(eval(f"'{contents}'"))
    else:
        f.write(contents)
    f.close()

def pathFormatted(string):
    global unnamedIndex, unnamed
    return string.replace('\\', '!').replace('/', '!').replace(':', '!').replace('*', '!').replace('?', '!').replace('"', '!').replace('<', '!').replace('>', '!').replace('|', '!') if string else (f"unnamed_{(unnamed := unnamedIndex)}")

def makeDir(path):
    global directory
    try:
        os.makedirs(f"{directory}/{path}")
    except:
        pass

makeDir("library")
directory += "/library"
makeDir("trinkets")
makeDir("folders")
directory += "/trinkets"

for i in f["trinkets"]:
    makeDir(pathFormatted(i['name']))
    for o in i["code"]:
        makeFile(f"{pathFormatted(i['name'])}/{pathFormatted(o['name'])}", o["code"], False)
        if unnamed:
            unnamedIndex += 1
            unnamed = 0

directory = directory[:-9:] + "/folders"

for i in f["folders"]:
    makeDir(pathFormatted(i))
    unnamedIndex = 1
    for o in f["folders"][i]:
        makeDir(f"{pathFormatted(i)}/{pathFormatted(o['name'])}")
        for u in o["code"]:
            makeFile(f"{pathFormatted(i)}/{pathFormatted(o['name'])}/{pathFormatted(u['name'])}", u["code"], False)
            if unnamed:
                unnamedIndex += 1
                unnamed = 0
