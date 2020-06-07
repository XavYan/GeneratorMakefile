#!/usr/bin/env python3

import sys
import gmk

if len(sys.argv) != 2:
    print("ERROR! Incorrect options. See --help for more information")
    exit(1)

gmk.generateMakefile(sys.argv[1])