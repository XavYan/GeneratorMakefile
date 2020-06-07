CC=g++
INCLUDE=include
SRC=src
BIN=bin
INCLUDE=include
FILENAME=fracciones
EXECUTABLE=mani
EXINCLUDE=h
EXSRC=cpp
binary.o: binary.$(EXINCLUDE) binary.$(EXSRC)
	$(CC) $(CCFLAGS) -c -o binary.o $(SRC)/binary.$(EXSRC)
all: binary.o hpair.$(EXINCLUDE) $(EXECUTABLE).$(EXSRC)
	$(CC) $(CCFLAGS) -o $(FILENAME) binary.o $(EXECUTABLE).$(EXSRC)
clean:
	rm -rf *.o
.PHONY: clean
