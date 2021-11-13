#!/usr/bin/env python3

import json
import hashlib
import urllib.request
import os

t = 0
entry = ""

md5 = hashlib.md5()


def getHash(name):

    with open (name,'rb') as f:
        for line in f:
            md5.update(line)
    return md5.hexdigest()


def mod():

    t = 0

    dir = input("Please provide Version ID: ")

    url = input("Paste a Mod URL to create an entry for: ")

    while url != "":

        name = str(url.split("/")[-1])
        version = str(name.split("-")[-1])

        try:
            urllib.request.urlretrieve(url, name)
        except ConnectionRefusedError:
            print("Please check your Internet connection!")
            if entry != "":
                print("Here's what you've got so far:\n \n”"+entry)
            quit

        hash = getHash(name)
        size = os.path.getsize(name)

        if t == 0:
            distr = str(json.dumps({
            "name": name,
            "id": dir,
            "type": "Mod",
            "artifact": {
                "url": url,
                "size": size,
                "MD5": hash,
                "path": dir+"/" + name
                }
            }),)
            entry = distr

        else:
            distr = str(";"+json.dumps({
            "name": name,
            "id": dir,
            "type": "Mod",
            "artifact": {
                "url": url,
                "size": size,
                "MD5": hash,
                "path": dir+"/" + name
                }
            }),)
            entry = str(entry)+str(distr)

        os.system("rm "+ name)
        print("Added", name)
        url = input("\nPaste the next mod URL to create an entry for, \nor press enter to exit: ")
        t += 1

    print("Successfully generated distribution index entries for",t,"mods in Version",dir+"!")
    del list(entry)[0]
    entry = str(entry).replace("'","")

    if "blob" in entry:
        entry = entry.replace("blob", "raw")

    entry = entry.replace(")", "")
    entry = entry.replace(";", ",\n")
    print(entry.replace("(", "")[0:])

def File():

    url = input("Paste a File URL to create an entry for: ")

    while url != "":

        name = str(url.split("/")[-1])
        version = str(name.split("-")[-1])

        urllib.request.urlretrieve(url, name)

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
                "path": "config/" + name
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
                "path": "config/" + name
                }
            }),)
            entry = str(entry)+str(distr)

        os.system("rm "+ name)
        print("Added", name)
        url = input("\nPaste the next File URL to create an entry for, \nor press enter to exit: ")
        t += 1

    print("Successfully generated distribution index entries for",t,"Files!")
    del list(entry)[0]
    entry = str(entry).replace("'","")

    if "blob" in entry:
        entry = entry.replace("blob", "raw")

    entry = entry.replace(")", "")
    entry = entry.replace(";", ",\n")
    print(entry.replace("(", "")[0:])

run = input("Type to generate: Mod (1) or (Config)File (2): ")
if run == "2":
    File()
if run == "1":
    mod()
else:
    print("Please provide either 1 or 2! You provided", run)

