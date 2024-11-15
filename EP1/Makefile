# Compilador
CXX = g++

# Flags de compilação
CXXFLAGS = -Iinclude -Wall -Wextra -std=c++17

# Arquivos fonte
SRCS = src/main.cpp src/passa_tempo.cpp src/thread_class.cpp src/thread_functions.cpp

# Arquivos objeto
OBJS = $(SRCS:.cpp=.o)

# Nome do executável
EXEC = EP1

# Regra padrão: build
all: build

# Regra de build: compila e gera o executável
build: $(EXEC)

# Linka os arquivos objeto para criar o executável
$(EXEC): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Compila os arquivos fonte em objetos
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Regra para rodar o programa
run: build
	./$(EXEC)

# Regra para limpar os arquivos gerados
clean:
	rm -f $(EXEC) $(OBJS)

# Declaração de targets que não correspondem a arquivos
.PHONY: all build run clean
