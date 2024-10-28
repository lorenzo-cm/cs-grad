# Variables
CC = g++
CFLAGS = -Wall -Wextra -Iinclude
SRCDIR = src
BUILDDIR = build
INCLUDEDIR = include
TARGET = program

# Source and Object Files
SOURCES = $(SRCDIR)/main.cpp $(SRCDIR)/thread_class.cpp $(SRCDIR)/thread_functions.cpp $(SRCDIR)/passa_tempo.cpp
OBJECTS = $(patsubst $(SRCDIR)/%.cpp, $(BUILDDIR)/%.o, $(SOURCES))

# Default Target
all: $(TARGET)

# Build Target
$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^

# Ensure Build Directory Exists
$(OBJECTS): | $(BUILDDIR)

$(BUILDDIR):
	mkdir -p $(BUILDDIR)

# Compile Object Files with Dependencies
$(BUILDDIR)/main.o: $(SRCDIR)/main.cpp $(INCLUDEDIR)/thread_functions.hpp $(INCLUDEDIR)/thread_class.hpp
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILDDIR)/thread_class.o: $(SRCDIR)/thread_class.cpp $(INCLUDEDIR)/thread_class.hpp
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILDDIR)/thread_functions.o: $(SRCDIR)/thread_functions.cpp $(INCLUDEDIR)/thread_functions.hpp
	$(CC) $(CFLAGS) -c $< -o $@

$(BUILDDIR)/passa_tempo.o: $(SRCDIR)/passa_tempo.cpp
	$(CC) $(CFLAGS) -c $< -o $@

# Clean Target
clean:
	rm -f $(BUILDDIR)/*.o $(TARGET)
