CC = g++
CFLAGS = -std=c++11 -g -Wall -pg

INCLUDE_DIR = include
BIN_DIR = bin
OBJ_DIR = obj
SRC_DIR = src
OUT_DIR = out
SAMPLE_DIR = sample

SOURCES := $(shell find $(SRC_DIR) -name '*.cpp')
OBJECTS := $(subst $(SRC_DIR),$(OBJ_DIR),$(SOURCES:%.cpp=%.o))

ANALISAMEM = $(BIN_DIR)/analisamem

EXE = $(BIN_DIR)/$(PROG_NAME)
PROG_NAME = main

# generates exe file, executes gprof, and generates perf log
all: 
	@make -s gprof perf mem plot


# links objects and generates the executable
$(PROG_NAME): $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJ_DIR)/*.o -o $(BIN_DIR)/$@


# compiles single cpp file
$(OBJ_DIR)/%.o:	$(SRC_DIR)/%.cpp
	$(CC) -I $(INCLUDE_DIR) $(CFLAGS) -c $< -o $@


bin: $(PROG_NAME)


gprof: $(PROG_NAME) $(OUT_DIR)
	$(EXE) -i $(SAMPLE_DIR)/bolao.ppm -o $(OUT_DIR)/bolao.pgm -p $(OUT_DIR)/gprofBolao.out

	gprof $(BIN_DIR)/$(PROG_NAME) gmon.out > out/gprofBolao.txt


perf: $(PROG_NAME) $(OUT_DIR)
	$(EXE) -i $(SAMPLE_DIR)/bolao.ppm -o $(OUT_DIR)/bolao.pgm -p $(OUT_DIR)/perfBolao.out


mem: $(PROG_NAME) $(OUT_DIR) analisamem
	$(EXE) -i $(SAMPLE_DIR)/bolao.ppm -o $(OUT_DIR)/bolao.pgm -p $(OUT_DIR)/memBolao.out -l

	$(ANALISAMEM) -i $(OUT_DIR)/memBolao.out -p $(OUT_DIR)/anMemBolao.out


plot:
	gnuplot $(OUT_DIR)/*.gp


analisamem:
	gcc -I $(INCLUDE_DIR) -g $(SRC_DIR)/analisamem.c $(SRC_DIR)/pilhaindexada.c -o $(BIN_DIR)/analisamem


# makes out dir
out:
	if test -d $(OUT_DIR); then rm -rf $(OUT_DIR); fi
	mkdir $(OUT_DIR)


snailandblackbuck: $(PROG_NAME) $(OUT_DIR)
	$(EXE) -i $(SAMPLE_DIR)/images/snail.ppm -o $(OUT_DIR)/snail.pgm -p $(OUT_DIR)/perfSnail.out
	$(EXE) -i $(SAMPLE_DIR)/images/blackbuck.ppm -o $(OUT_DIR)/blackbuck.pgm -p $(OUT_DIR)/perfBlackbuck.out


# runs valgrind (for debug)
valgrind:
	valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose --log-file=valgrind-out.txt $(BIN_DIR)/$(PROG_NAME)


# make the directories clean
clean:
	@rm -rf *.out $(OBJ_DIR)/* $(BIN_DIR)/* gmon.out *.pgm *.txt -r out