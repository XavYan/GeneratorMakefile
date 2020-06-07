import re
from . import makefileGen as mg

rSettings = r"set ([\w-]+) *: *([\w/\\.]+)"
rPhony = r"module ([\w-]+) phony *: *(.*)"

def removeEmptyLines (filename, newFilename):
    container = list()
    with open(filename, "r") as file:
        for line in file:
            if line.strip():
                container.append(line)

    with open(newFilename, "w") as nfile:
        nfile.writelines(container)

    return newFilename


def initializeMakefile (makefile):
    with open(makefile, "w") as mk:
        mk.write("CC=g++\n")
        mk.write("INCLUDE=.\n")
        mk.write("SRC=.\n")
        mk.write("BIN=.\n")
        mk.write("CCFLAGS=-g -Wall -Wextra -I$(INCLUDE) --std=c++17\n")
        mk.write("FILENAME=main\n")
        mk.write("EXECUTABLE=main\n")
        mk.write("EXINCLUDE=h\n")
        mk.write("EXSRC=cpp\n")

def gmkProcess (makefile, line):
    instruction = line.split()[0]
    if instruction == "set":
        processSetting(makefile, line)
    elif instruction == "require":
        processRequire(makefile, line)
    elif instruction == "module":
        processModule(makefile, line)
    elif instruction == "active":
        pass
    else:
        print("ERROR! Instruction {} not valid".format(instruction))

def processSetting (makefile, line):
    """set instruction has this syntax: set [setting]: value"""
    # Let's interpret the setting
    setting = re.search(rSettings, line)
   
    # Getting all necessary data
    source = setting[1]
    value = setting[2]

    # Applying configuration
    mg.applyConfiguration(makefile, source, value)


def processRequire (makefile, line):
    """require instruction has this syntax: require [template] [file]"""
    # Like template action is optional, we need to know if it has it
    sline = line.split()
    if "template" in line:
        mg.createTemplateModule (makefile, sline[2])
    else:
        mg.createSourceModule (makefile, sline[1])

def processModule (makefile, line):
    """syntax for module instruction: module [name] [compile [file]]"""
    sline = line.split()
    if "compile" in sline:
        filename = ""
        if len(sline) == 4:
            filename = sline[3]
        mg.createModule(makefile, sline[1], filename)
    elif "phony:" in sline:
        rline = re.search(rPhony, line)
        mg.createPhonyModule(makefile, rline[1], rline[2])