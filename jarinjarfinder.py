#!/usr/bin/env python
from zipfile import ZipFile
import os


# gets files in the current folder
files = os.listdir()

# keep the mod files
remove = []
for filename in files:
    if filename[-4:] != ".jar":
        remove.append(filename)
for file in remove:
    files.remove(file)

with open("jijfiles.log", "w") as log:
    log.write("Jar in Jar Mods:\n")

# check in each mod file for jar in jar mods
for mod_file in files:
    with ZipFile(mod_file, 'r') as jar:
        try:
            # get the file containing locations of any jij mods
            data = str(jar.read("META-INF/jarjar/metadata.json"))
            lines = data.split("\\n")
            with open("jijfiles.log", "a") as log:
                for line in lines:
                    # get mod name
                    if '"artifact"' in line:
                        log.write(line.replace('\\r', "").replace('"artifact": ', "") + " from mod file " + mod_file + '\n')
                        print(line.replace('\\r', "").replace('"artifact": ', ""), "from mod file", mod_file)
        except KeyError:
            pass

with open("jijfiles.log", "a") as log:
    log.write("All mods scanned. There could be jars in jars in jars, etc, but I have not scanned for them.\n")
    log.write("Made by Plite.")