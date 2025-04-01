CXX = g++
CXXFLAGS = -O1 -fno-omit-frame-pointer -g -Wall -Wshadow -std=c++20 -Wno-unused-result -Wno-sign-compare -Wno-char-subscripts #-fsanitize=address,undefined #-fuse-ld=gold

.PHONY: all clean

bin:
	mkdir bin

%: %.cpp bin
	$(CXX) $(CXXFLAGS) $< -o bin/$(notdir $@)

clean:
	rm bin ent.txt out.txt -rf