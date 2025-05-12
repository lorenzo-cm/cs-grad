#include "reader.hpp"
#include <stdexcept>

void Reader::readN(char* filename){
    std::ifstream file(filename);
    size = 0;
    if(!file) throw std::runtime_error("Cannot open the file");
    file >> size;
    for(int i = 0; i < size; i++){
        file >> valuesN[i];
    }
    file.close();
}


void Reader::printN(){
    for(int i = 0; i<size; i++) printf("%d ", valuesN[i]);
    putchar('\n');
}