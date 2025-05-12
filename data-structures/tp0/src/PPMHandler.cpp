#include "PPMHandler.h"
#include "msgassert.h"
#include "memlog.h"
#include <fstream>
#include <cstdio>
#include <cmath>

void readPPM(Matrix& matrix, std::string filename){

    std::ifstream file(filename);
    std::string text;

    erroAssert(file.is_open(), "Error in file opening");

    std::string type;
    file >> type;
    erroAssert(type == "P3", "Incorret type (not P3)");

    size_t rows, cols;
    file >> cols >> rows;

    matrix.createMatrix(rows, cols);

    unsigned range;
    file >> range;

    erroAssert(range == 255, "different RGB limit ");

    //read all rgb lines
    for(unsigned i = 0; i<matrix.getRows(); i++){
        for(unsigned j = 0; j<matrix.getCols(); j++){
            unsigned red,green,blue;
            file >> red >> green >> blue;

            matrix.setValue(i, j, RGB(red, green, blue));
        }
    }

    file.close();
}

void writePGM(Matrix& matrix, std::string filename){

    std::ofstream file(filename);

    erroAssert(file.is_open(), "Error in file opening");

    // pgm 
    file << "P2" << std::endl;

    // cols rows
    file << matrix.getCols() << " " << matrix.getRows() << std::endl;

    // rgb range
    file << "49" << std::endl;

    turnBW(matrix, file);
    
    file.close();

}


void turnBW(Matrix& matrix, std::ofstream& file){
    erroAssert(file.is_open(), "Error in file opening");
    
    for(unsigned i = 0; i<matrix.getRows(); i++){
        for(unsigned j = 0; j<matrix.getCols(); j++){

            unsigned y = 49 * (0.3 * (unsigned)matrix.getValue(i,j).r + 0.59 * (unsigned)matrix.getValue(i,j).g + 0.11 * (unsigned)matrix.getValue(i,j).b) / 255;

            if(j == matrix.getCols() -1){
                file << y;
                continue;
            }

            file << y << ' ';
        }
        file << std::endl;
    }
}