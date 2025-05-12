# Makefile for TP2
# by Lorenzo Carneiro Magalhaes



#* VARIABLES DECLARATION AND AMBIENT SETTING


CC = g++
CFLAGS = -std=c++17 -Wall -O3 # -g

INCLUDE_DIR = include
BIN_DIR = bin
OBJ_DIR = obj
SRC_DIR = src
OUT_DIR = out


C_INCLUDE = $(shell cd include;ls -d */) 
C_INCLUDE := $(subst $(C_INCLUDE), $(C_INCLUDE), $(C_INCLUDE:%=$(INCLUDE_DIR)/%)) $(INCLUDE_DIR)
C_INCLUDE := $(subst $(C_INCLUDE), $(C_INCLUDE), $(C_INCLUDE:%=-I %))


SOURCES := $(shell find $(SRC_DIR) -name '*.cpp')
OBJECTS := $(subst $(SRC_DIR),$(OBJ_DIR),$(SOURCES:%.cpp=%.o))

ANALISAMEM = $(BIN_DIR)/analisamem

EXE = $(BIN_DIR)/$(PROG_NAME)
PROG_NAME = main



#------------------------------------------------------------------------------------



#* TESTS


testexec: $(OUT_DIR) bin
	./bin/main -v 6 -m 1000 -k 3 -s 3315 -i src/examples/ent.txt -o out/results.out -p


testmem: $(OUT_DIR) analisamem

	@echo "---------------- Memory test ----------------"

	g++ $(C_INCLUDE) src/testMem.cc src/memlog.cpp -o bin/testMem
	
	@echo "----------------- quicksort -----------------"
	./bin/testMem -v 0 -m 5 -k 3 -s 333 -n 15
	$(ANALISAMEM) -i $(OUT_DIR)/quicksort.out -p $(OUT_DIR)/mem_quicksort.out

	@echo "------- median of k quicksort (k=3) ---------"
	./bin/testMem -v 1 -m 5 -k 3 -s 333 -n 15
	$(ANALISAMEM) -i $(OUT_DIR)/median_of_k_quicksort.out -p $(OUT_DIR)/mem_median_of_k_quicksort.out

	@echo "-------- selection m quicksort (m=3) --------"
	./bin/testMem -v 2 -m 5 -k 3 -s 333 -n 15
	$(ANALISAMEM) -i $(OUT_DIR)/selection_m_quicksort.out -p $(OUT_DIR)/mem_selection_quicksort.out

	@echo "---------- non recursive quicksort ----------"
	./bin/testMem -v 3 -m 5 -k 3 -s 333 -n 15
	$(ANALISAMEM) -i $(OUT_DIR)/non_recursive_quicksort.out -p $(OUT_DIR)/mem_non_recursive_quicksort.out

	@echo "------------ smart stack quicksort ----------"
	./bin/testMem -v 4 -m 5 -k 3 -s 333 -n 15
	$(ANALISAMEM) -i $(OUT_DIR)/smart_stack_quicksort.out -p $(OUT_DIR)/mem_smart_stack_quicksort.out

	@echo "----------------- mergesort -----------------"
	./bin/testMem -v 5 -m 5 -k 3 -s 333 -n 15

	@echo "----------------- heapsort ------------------"
	./bin/testMem -v 6 -m 5 -k 3 -s 333 -n 15



#* EXECUTES ALL


# generates exe file, executes gprof, and generates perf log
all: 
	@make -s clean bin_dir obj_dir bin testexec analisamem testmem plot



#* COMPILE


# links objects and generates the executable
$(PROG_NAME): $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJ_DIR)/*.o -o $(BIN_DIR)/$@


# compiles single cpp file
$(OBJ_DIR)/%.o:	$(SRC_DIR)/%.cpp
	$(CC) $(C_INCLUDE) $(CFLAGS) -c $< -o $@


bin: $(PROG_NAME)


binmem:
	g++ $(C_INCLUDE) src/testMem.cc src/memlog.cpp -o bin/testMem


#* OTHER FUNCTIONS

plot:
	gnuplot $(OUT_DIR)/*.gp


analisamem:
	gcc $(C_INCLUDE) -g $(SRC_DIR)/analisamem.c $(SRC_DIR)/pilhaindexada.c -o $(BIN_DIR)/analisamem

	
# runs valgrind (for debug)
valgrind:
	valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose --log-file=valgrind-out.txt ./bin/testMem -v 2 -m 5 -k 3 -s 333 -n 15



#* AUXILIARY FUNCTIONS


# makes out dir
out:
	@if test -d $(OUT_DIR); then rm -rf $(OUT_DIR); fi
	@mkdir $(OUT_DIR)

# makes bin dir
bin_dir:
	@mkdir $(BIN_DIR)

# makes obj dir
obj_dir:
	@mkdir $(OBJ_DIR)



#* CLEAN


# make the directories clean
clean:
	@rm -rf *.out $(OBJ_DIR)/* $(EXE) -r out *.gp *.gpdat *.png bin/* valgrind-out.txt
