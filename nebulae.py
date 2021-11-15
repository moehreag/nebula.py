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
    req = True

    dir = input("Please provide Version ID: ")

    url = input("Paste a Mod URL to create an entry for: ")

    req = input("Is the mod required? [Y/n]:")

    if "n" in req or "N" in req:
        req = False
        defreq = input("Should the Mod be enabled by default? [Y/n]")
        if "n" in defreq or "N" in defreq:
            defreq = False
        else:
            defreq = True

    else:
        req = True
        defreq = True

    while url != "":

        if "blob" in url:
            entry = entry.replace("blob", "raw")

        filename = str(url.split("/")[-1])
        name = str(filename.split("-")[:-1])
        name = str(name.replace("[", ""))
        name = str(name.replace("]", ""))
        name = str(name.replace("'",""))
        version = str(filename.split("-")[-1])
        ext = version.split(".")[-1]

        i = 0
        mv = ""

        while version.split(".")[i] != ext:
            mv += version.split(".")[i]
            if version.split(".")[i+1] != ext:
                mv += "."
            i = i+1

        try:
            urllib.request.urlretrieve(url, filename)
        except ConnectionRefusedError:
            print("Please check your Internet connection!")
            if entry != "":
                print("Here's what you've got so far:\n \n”"+entry)
            quit
        except URLError:
            print("Please check your pasted URL!")
            if entry != "":
                print("Here's what you've got so far:\n \n”"+entry)
            quit

        hash = getHash(filename)
        size = os.path.getsize(filename)

        if t == 0:
            distr = str(json.dumps({
            "name": name,
            "id": dir+":"+name+":"+mv,
            "type": "Mod",
            "required":{
                "value":req,
                "def":defreq,
                },
            "artifact": {
                "url": url,
                "size": size,
                "MD5": hash,
                "path": dir+"/" + filename
                }
            }),)
            entry = distr

        else:

            distr = str(";"+json.dumps({
            "name": name,
            "id": dir+":"+name+":"+mv,
            "type": "Mod",
            "required":{
                "value":req,
                "def":defreq,
                },
            "artifact": {
                "url": url,
                "size": size,
                "MD5": hash,
                "path": dir+"/" + filename
                }
            }),)
            entry = str(entry)+str(distr)

        os.remove(filename)
        print("Added", name, "with version", mv, "to", dir)
        url = input("\nPaste the next mod URL to create an entry for, \nor press enter to exit: ")
        t += 1

    print("Successfully generated distribution index entries for",t,"mods in Version",dir+"!\n")
    del list(entry)[0]
    entry = str(entry).replace("'","")

    entry = entry.replace(")", "")
    entry = entry.replace(";", ",\n")
    print(entry.replace("(", "")[0:])

def File():

    dir = input("Please provide Version ID: ")

    url = input("Paste a File URL to create an entry for: ")

    while url != "":

        if "blob" in url:
            entry = entry.replace("blob", "raw")

        name = str(url.split("/")[-1])
        version = str(name.split("-")[-1])

        urllib.request.urlretrieve(url, name)

        hash = getHash(name)
        size = os.path.getsize(name)

        if t == 0:
            distr = str(json.dumps({
            "name": name,
            "id": dir,
            "type": "File",
            "artifact": {
                "url": url,
                "size": size,
                "MD5": hash,
                "path": "config/" + filename
                }
            }),)
            entry = distr

        else:
            distr = str(";"+json.dumps({
            "name": name,
            "id": dir,
            "type": "File",
            "artifact": {
                "url": url,
                "size": size,
                "MD5": hash,
                "path": "config/" + filename
                }
            }),)
            entry = str(entry)+str(distr)

        os.remove(name)
        print("Added", name)
        url = input("\nPaste the next File URL to create an entry for, \nor press enter to exit: ")
        t += 1

    print("Successfully generated distribution index entries for",t,"Files!\n")
    del list(entry)[0]
    entry = str(entry).replace("'","")

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

