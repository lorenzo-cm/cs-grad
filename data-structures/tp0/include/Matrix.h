// Implemented to make the matrix manipulation easier
// It creates a class representing a matrix
// The class deals with RGB type only

#ifndef MATRIX_H
#define MATRIX_H

#include <iostream>
#include "RGB.h"

class Matrix{

    private:
        static unsigned id;
        size_t rows = 0;
        size_t cols = 0;
        RGB** matrix = nullptr;

    public:

        Matrix();
        Matrix(size_t sizex, size_t sizey);
        ~Matrix();

        void setRowsCols(size_t rows, size_t cols);
        
        void createMatrix();
        void createMatrix(size_t sizex, size_t sizey);

        size_t getRows();
        size_t getCols();

        void delMatrix();

        RGB getValue(size_t row, size_t col);
        void setValue(size_t row, size_t col, RGB value);

        void print();

        friend std::ostream& operator << (std::ostream& os, Matrix& matrix);

};

#endif