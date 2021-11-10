#!/usr/bin/env python3

import json
import hashlib
import urllib.request
import os

t = 0
url = input("Paste a Mod URL to create an entry for: ")

md5 = hashlib.md5()


def getHash(file):

    with open (name,'rb') as f:
        for line in f:
            md5.update(line)
    return md5.hexdigest()



while url != "":

    name = str(url.split("/")[-1])
    version = str(name.split("-")[-1])

    urllib.request.urlretrieve(url, name)

    #hash = md5(name).hexdigest()
    hash = getHash(name)
    size = os.path.getsize(name)
    
    if t == 0:
        distr = str(json.dumps({
        "name": name,
        "id": name,
        "type": "File",
        "artifact": {
            "url": url,
            "size": size,
            "MD5": hash,
            "path": "mods/" + name
            }
        }),)
        entry = distr
    
    else:
        distr = str(";"+json.dumps({
        "name": name,
        "id": name,
        "type": "File",
        "artifact": {
            "url": url,
            "size": size,
            "MD5": hash,
            "path": "mods/" + name
            }
        }),)
        entry = str(entry)+str(distr)

    os.system("rm "+ name)
    print("Added", name)
    url = input("\nPaste the next mod URL to create an entry for, \nor press enter to exit: ")
    t += 1        

print("Successfully generated distribution index entries for",t,"mods!")
del list(entry)[0]
entry = str(entry).replace("'","")
entry = entry.replace(")", "")
entry = entry.replace(";", ",\n")
print(entry.replace("(", "")[0:])
