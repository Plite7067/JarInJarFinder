#!/usr/bin/env python
import os
from zipfile import ZipFile

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
    def recursive_func(mod_file, indent):
        indent_space = "    "
        with ZipFile(mod_file, 'r') as jar:
            try:
                # get the file containing locations of any jij mods
                data = str(jar.read("META-INF/jarjar/metadata.json"))
                lines = data.split("\\n")
                for line in lines:
                    # get mod name
                    if '"artifact"' in line:
                        name = jar.filename.rsplit('/', 1)[-1]
                        log.write((indent_space * indent) + (line.replace('\\r', "").replace('"artifact": ',
                                                                                             "") + " from mod file " + name).strip() + '\n')
                        print((indent_space * indent) + (
                                    line.replace('\\r', "").replace('"artifact": ', "") + " from mod file " + name).strip())
                    if '"path"' in line:
                        path = line.replace('",', "").replace('"path": "', "").strip().replace("\\r", "").replace('"', "")
                        jijmod = jar.open(path)
                        recursive_func(jijmod, indent + 1)
            except KeyError:
                pass


    for file in files:
        recursive_func(file, 1)
    log.write("All mods scanned.\n")
    log.write("Made by Plite.")
