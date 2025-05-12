CC=g++
CFLAGS=-std=c++11 -Wall -Wextra -O2
LDFLAGS= -lsqlite3

FILES = database databaseController loginManager mailbox matchGenerator menu pca user main
TEST_FILES = loginTest matchTest

INCLUDE_DIR=./include
SRC_DIR=./src
BUILD_DIR=./build
DOC_DIR=./doctest

# runs valgrind
valgrindMain:
	valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes --verbose --log-file=valgrind-out.txt ./main

# executes all the objects and executes main
exeFinder: ${SRC_DIR}/main.cpp
	g++ -std=c++11 ${BUILD_DIR}/*.o ${LDFLAGS} -o finder

# compiles all cpp's and makes the main and executes main
finder: ${SRC_DIR}/main.cpp
	g++ -std=c++11 -I ${INCLUDE_DIR} -I ${INCLUDE_DIR}/eigen ${SRC_DIR}/*.cpp ${LDFLAGS} -o finder

# compiles all files
# it works better for bash
buildAll:
	@mkdir build -p; \
	for file in ${FILES}; do\
		make $$file.o -s; \
	done

# compiles the cpp files in the source directory
%.o: ${SRC_DIR}/%.cpp
	${CC} -std=c++11 -I ${INCLUDE_DIR} -I ${INCLUDE_DIR}/eigen -c $< -o ${BUILD_DIR}/$@

# makes the match test
matchTest:
	g++ -std=c++11 -I ${INCLUDE_DIR} -I ${INCLUDE_DIR}/eigen ${BUILD_DIR}/matchGenerator.o ${BUILD_DIR}/database.o ${BUILD_DIR}/databaseController.o ${BUILD_DIR}/pca.o ${DOC_DIR}/matchTest.cpp ${LDFLAGS} -o matchTest

# makes the login test OBS: have to change main.cpp to another dir
loginTest:
	rm build/main.o; \
	g++ -std=c++11 -I ${INCLUDE_DIR} -I ${INCLUDE_DIR}/eigen ${DOC_DIR}/loginTest.cpp ${BUILD_DIR}/*.o ${LDFLAGS} -o loginTest

# makes the mailbox test
mailboxTest:
	rm build/main.o; \
	g++ -std=c++11 -I ${INCLUDE_DIR} -I ${INCLUDE_DIR}/eigen ${DOC_DIR}/mailboxTest.cpp ${BUILD_DIR}/*.o ${LDFLAGS} -o mailboxTest

# delete the main executable and all .o files
clean:
	@rm main -f; \
	find . -iwholename "${BUILD_DIR}/*.o" -exec rm {} \;