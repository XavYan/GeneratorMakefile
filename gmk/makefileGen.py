sourceModuleList = list()
sourceModuleTemplateList = list()

sourceSettings = {
    "sourcepath": "SRC",
    "headerpath": "INCLUDE",
    "binpath":    "BIN",
    "name":       "FILENAME",
    "executable": "EXECUTABLE",
    "exsrc":      "EXSRC",
    "exinc":      "EXINCLUDE"
}


def applyConfiguration (filename, source, value):
    container = list()

    print("Processing {} source with new value {}".format(source, value))

    # Set source we are looking for
    searchSource = ""
    # if source == "sourcepath":
    #     searchSource = "SRC"
    # elif source == "headerpath":
    #     searchSource = "INCLUDE"
    # elif source == "binpath":
    #     searchSource = "BIN"
    # elif source == "name":
    #     searchSource = "FILENAME"
    if source in sourceSettings:
        searchSource = sourceSettings[source]
    else:
        print("ERROR! Source not valid")
        exit(2)

    # Search for desired line
    with open(filename, "r") as file:
        for line in file:
            # print("Reading line: '{}'".format(line.strip()))
            if searchSource in line and not "EX" + searchSource in line:
                newLine = searchSource + "=" + value + "\n"
                # print("Adding '{}' new line".format(newLine.strip()))
                container.append(newLine)
            else:
                # print("Adding '{}' line".format(line.strip()))
                container.append(line)

    with open(filename, "w") as file:
        file.writelines(container)

def addPhonySource (makefile, name):
    container = list()
    exists = False
    with open(makefile, "r") as file:
        for line in file:
            if ".PHONY:" in line:
                exists = True
                container.append(line.strip() + " " + name + '\n')
            else:
                container.append(line)
        if not exists:
            container.append(".PHONY: " + name + '\n')

    with open(makefile, "w") as file:
        file.writelines(container)

def createTemplateModule (makefile, module):
    sourceModuleTemplateList.append(module)

def createSourceModule (makefile, module):
    sourceModuleList.append(module)

    container = list()

    container.append("{}.o: {}.$(EXINCLUDE) {}.$(EXSRC)\n".format(module, module, module))
    container.append("\t$(CC) $(CCFLAGS) -c -o {}.o $(SRC)/{}.$(EXSRC)\n".format(module, module))

    with open(makefile, "a") as file:
        file.writelines(container)

def createModule (makefile, name, filename = ""):
    programName = ""
    if filename == "":
        programName = "$(FILENAME)"
    else:
        programName = filename
    
    container = list()

    header = name + ":"
    for element in sourceModuleList:
        header += " {}.o".format(element)

    for element in sourceModuleTemplateList:
        header += " {}.$(EXINCLUDE)".format(element)

    header += " $(EXECUTABLE).$(EXSRC)\n"

    content = "\t$(CC) $(CCFLAGS) -o {}".format(programName)

    for element in sourceModuleList:
        content += " {}.o".format(element)

    content += " $(EXECUTABLE).$(EXSRC)\n"

    container.append(header)
    container.append(content)

    with open(makefile, "a") as file:
        file.writelines(container)

def createPhonyModule (makefile, name, action):
    # Creating module
    with open(makefile, "a") as file:
        container = "{}:\n".format(name)
        container += "\t{}\n".format(action)
        file.write(container)

    addPhonySource(makefile, name)