#!/usr/bin/env python3

import json

#entry = ""
t = 0
url = input("Paste a Mod URL to create an entry for: ")

while url != "":

    name = str(url.split("/")[-1])
    
    if t == 0:
        distr = str(json.dumps({"id":"mod","type":"File","artifact": {"url": url,"path":"mods/"+name}}),)
        entry = distr
    
    else:
        distr = str(";"+json.dumps({"id":"mod","type":"File","artifact": {"url": url,"path":"mods/"+name}}),)
        entry = str(entry)+str(distr)
        
    print("Added", name)
    url = input("\nPaste the next mod URL to create an entry for, \nor press enter to exit: ")
    t += 1        

print("Successfully generated distribution index entries for",t,"mods!")
del list(entry)[0]
print(entry,"\n\n\n")
entry = str(entry).replace("'","")
entry = entry.replace(")", "")
entry = entry.replace(";", "\n")
print(entry.replace("(", "")[0:])
