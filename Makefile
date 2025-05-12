# Makefile for TP3
# by Lorenzo Carneiro Magalhaes



#* VARIABLES DECLARATION AND AMBIENT SETTING


CC = g++
CFLAGS = -std=c++17 -Wall -O3 -g

INCLUDE_DIR = include
BIN_DIR = bin
OBJ_DIR = obj
SRC_DIR = src
OUT_DIR = out
TESTS_DIR = src/tests

SOURCES := $(shell find $(SRC_DIR) -name '*.cpp')
OBJECTS := $(subst $(SRC_DIR),$(OBJ_DIR),$(SOURCES:%.cpp=%.o))

ANALISAMEM = $(BIN_DIR)/analisamem

EXE = $(BIN_DIR)/$(PROG_NAME)
PROG_NAME = main



#------------------------------------------------------------------------------------



#* TESTS

exectest: out bin

	./$(BIN_DIR)/main -i $(TESTS_DIR)/input_05.txt -o $(OUT_DIR)/out.txt -t hash

	diff $(OUT_DIR)/out.txt $(TESTS_DIR)/output_05.txt

	./$(BIN_DIR)/main -i $(TESTS_DIR)/input_05.txt -o $(OUT_DIR)/out.txt -t tree

	diff $(OUT_DIR)/out.txt $(TESTS_DIR)/output_05.txt

	

#* EXECUTES ALL


# generates exe file and generates perf log
all: out
	@make -s clean bin exectest



#* COMPILE


# links objects and generates the executable
$(PROG_NAME): $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJ_DIR)/*.o -o $(BIN_DIR)/$@


# compiles single cpp file
$(OBJ_DIR)/%.o:	$(SRC_DIR)/%.cpp
	$(CC) -I $(INCLUDE_DIR) $(CFLAGS) -c $< -o $@


bin: $(PROG_NAME)


#* OTHER FUNCTIONS

# plot:
# 	gnuplot $(OUT_DIR)/*.gp


# analisamem:
# 	gcc $(C_INCLUDE) -g $(SRC_DIR)/analisamem.c $(SRC_DIR)/pilhaindexada.c -o $(BIN_DIR)/analisamem

	
# runs valgrind (for debug)
valgrind:
	valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose --log-file=valgrind-out.txt ./$(BIN_DIR)/main -i ent.txt -o $(OUT_DIR)/out.txt -t tree


#* AUXILIARY FUNCTIONS


# makes out dir
out:
	@if test -d $(OUT_DIR); then rm -rf $(OUT_DIR); fi
	@mkdir $(OUT_DIR)



#* CLEAN


# make the directories clean
clean:
	@rm -rf *.out $(OBJ_DIR)/* $(EXE) -r out *.gp *.gpdat *.png bin/* valgrind-out.txt