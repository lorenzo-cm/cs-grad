# Compilador
CXX = g++

# Diretórios
SRC_DIR = src
INCLUDE_DIR = include
BUILD_DIR = build

# Flags de compilação
CXXFLAGS = -I$(INCLUDE_DIR) -Wall -Wextra -pthread -std=c++17

# Lista de arquivos fonte
SRCS = $(wildcard $(SRC_DIR)/*.cpp)

# Lista de arquivos objeto (salvos em build/)
OBJS = $(patsubst $(SRC_DIR)/%.cpp,$(BUILD_DIR)/%.o,$(SRCS))

# Nome do executável
EXEC = EP1

# Regra padrão: build
all: $(EXEC)

# Linka os arquivos objeto para criar o executável
$(EXEC): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $^

# Compila os arquivos fonte em objetos dentro de build/
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Regra para rodar o programa
run: $(EXEC)
	./$(EXEC)

# Regra para limpar os arquivos gerados
clean:
	rm -rf $(EXEC) $(BUILD_DIR)

# Declaração de targets que não correspondem a arquivos
.PHONY: all run clean
