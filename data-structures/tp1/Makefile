CC = g++
CFLAGS = -std=c++11 -Wall -pg -g

INCLUDE_DIR = include
BIN_DIR = bin
OBJ_DIR = obj
SRC_DIR = src
OUT_DIR = out
TESTS_DIR = src/tests

SOURCES := $(shell find $(SRC_DIR) -name '*.cpp')
OBJECTS := $(subst $(SRC_DIR),$(OBJ_DIR),$(SOURCES:%.cpp=%.o))

EXE = $(BIN_DIR)/$(PROG_NAME)
PROG_NAME = main

# generates exe file and makes the test cases
all: 
	@make -s bin test gprof


# makes the program run
make run:
	@make -s bin
	@./$(EXE)


# links objects and generates the executable
$(PROG_NAME): $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJ_DIR)/*.o -o $(BIN_DIR)/$@


# compiles single cpp file
$(OBJ_DIR)/%.o:	$(SRC_DIR)/%.cpp
	$(CC) -I $(INCLUDE_DIR) $(CFLAGS) -c $< -o $@


# creates the executable and the out dir
bin: $(PROG_NAME) $(OUT_DIR)
	

# runs all the tests
test: $(PROG_NAME) $(OUT_DIR)
	$(foreach test, $(wildcard $(TESTS_DIR)/*) , \
		$(shell $(EXE) $(subst $(TESTS_DIR), $(OUT_DIR), $(test:%.txt=%.out) ) < $(test) > $(OUT_DIR)/$(notdir $(test))) 	\
	)


# runs gprof
gprof: $(PROG_NAME) $(OUT_DIR)
	@$(EXE) < $(TESTS_DIR)/cr10000e10000l10000.txt > out/gprof.txt
	@gprof $(BIN_DIR)/$(PROG_NAME) gmon.out > out/gprof.txt


# makes out dir
out:
	if test -d $(OUT_DIR); then rm -rf $(OUT_DIR); fi
	mkdir $(OUT_DIR)


# runs valgrind (for debug)
# when running valgrind, comment -pg flag in CFLAGS
memcheck: $(PROG_NAME) $(OUT_DIR)
	valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose --log-file=valgrind-out.txt $(BIN_DIR)/$(PROG_NAME) < $(TESTS_DIR)/cr10e10l10.txt
	

# make the directories clean
clean:
	@rm -rf *.out $(OBJ_DIR)/* $(BIN_DIR)/* gmon.out *.txt -r out write