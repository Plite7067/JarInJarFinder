#!/usr/bin/env python
import os
import json
from zipfile import ZipFile
from time import sleep

# gets files in the current folder
files = os.listdir()

# remove non-mod files
remove = []
for filename in files:
    if filename[-4:] != ".jar":
        remove.append(filename)
for file in remove:
    files.remove(file)

# create the log file
with open("jijfiles.log", "w") as log:
    print("Scanning...")
    # adds a tiny delay, to increase 'perceived value'
    sleep(0.2)
    log.write("Jar in Jar Mods:\n")

# check in each mod file for jar in jars. ZipFile can accept file names or files. Equivalent of open for zip/jar files.
    def recursive_func(mod_file, indent):
        indent_space = "    "
        with ZipFile(mod_file, 'r') as jar:
            try:
                # get the file containing locations of any jij mods
                data = jar.read("META-INF/jarjar/metadata.json").decode('utf8')
                # deserialise the json
                jij_data = json.loads(data)
                if indent == 1 and len(jij_data['jars']) != 0:
                    log.write('\n' + mod_file + '\n')
                for mod_no in range(0, len(jij_data['jars'])):
                    artifact = jij_data['jars'][mod_no]['identifier']['artifact']
                    name = jar.filename.rsplit('/', 1)[-1]
                    # write mod name to log
                    log.write((indent_space * indent) + (artifact + " from mod file " + name).strip() + '\n')
                    # go into mod to check for new mods
                    path = jij_data['jars'][mod_no]['path']
                    recursive_func(jar.open(path), indent + 1)
            # this fires if a mod has no jar in jar mods.
            except KeyError:
                pass

    # starts the scan
    for file in files:
        recursive_func(file, 1)
    log.write("\nAll mods scanned.\n")
    log.write("Made by plite7067.")
print("Done. See jijfiles.log for the list of jar in jar mods.")
