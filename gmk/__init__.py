import sys
from os import remove

from . import gmkProcessing as gp

def generateMakefile (filename, makefile = "Makefile"):
    filename = gp.removeEmptyLines(filename, "/tmp/" + filename + ".gmk.tmp")

    gp.initializeMakefile(makefile)

    with open(filename, "r") as file:
        for line in file:
            if line.strip()[0] != '#':
                gp.gmkProcess(makefile, line)

    # Deleting temporary file
    remove(filename)