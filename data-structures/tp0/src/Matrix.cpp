#include "Matrix.h"
#include "msgassert.h"
#include "memlog.h"

unsigned Matrix::id = -1;

/**
 * @brief Construct a new Matrix:: Matrix object
 * 
 * @param sizex rows
 * @param sizey cols
 */
Matrix::Matrix(size_t sizex, size_t sizey){
    id++;

    rows = sizex;
    cols = sizey;
    createMatrix();
}


/**
 * @brief Construct a new Matrix< T>:: Matrix object
 */
Matrix::Matrix(){
    id++;
}


/**
 * @brief Destroy the Matrix<T>:: Matrix object
 */
Matrix::~Matrix(){
    if(matrix) delMatrix();
}


/**
 * @brief Create the matrix structure
 */
void Matrix::createMatrix(){
    if(rows == 0) return;
    if(cols == 0) return;

    if(matrix) delMatrix();

    matrix = new RGB*[rows];
    for(size_t i = 0; i<rows; i++){
        matrix[i] = new RGB[cols];
    }
}


void Matrix::createMatrix(size_t sizex, size_t sizey){

    if(matrix) delMatrix();

    rows = sizex;
    cols = sizey;

    matrix = new RGB*[rows];
    for(size_t i = 0; i<rows; i++){
        matrix[i] = new RGB[cols];
    }
}


/**
 * @brief Set the number of rows and columns for future matrix construction
 * 
 * @param sizex number of rows
 * @param sizey number of cols
 */
void Matrix::setRowsCols(size_t sizex, size_t sizey){
    rows = sizex;
    cols = sizey;
}


/**
 * @brief get the number of rows
 * 
 * @return size_t* size
 */
size_t Matrix::getRows(){
    return rows;
}


/**
 * @brief get the number of columns
 * 
 * @return size_t* size
 */
size_t Matrix::getCols(){
    return cols;
}


/**
 * @brief Deletes the dynamic matrix
 */
void Matrix::delMatrix(){

    erroAssert(matrix, "Null matrix pointer");

    for(size_t i = 0; i<rows; i++){
        delete [] matrix[i];
    }
    delete [] matrix;

    matrix = nullptr;

}

/**
 * @brief Set a value of certain type in the determined position
 * 
 * @param row
 * @param col
 * @param value 
 */
void Matrix::setValue(size_t row, size_t col, RGB value){
    erroAssert(matrix, "Null matrix pointer");

    ESCREVEMEMLOG((long)&matrix[row][col], sizeof(RGB), this->id);

    matrix[row][col] = value;
}


/**
 * @brief Get a value of certain type in the determined position
 * 
 * @param row
 * @param col
 */
RGB Matrix::getValue(size_t row, size_t col){

    erroAssert(matrix, "Null matrix pointer");

    LEMEMLOG((long)&matrix[row][col], sizeof(RGB), this->id);

    return matrix[row][col];
}


/**
 * @brief prints the matrix
 */
void Matrix::print(){

    erroAssert(matrix, "Null matrix pointer");
    
    for(unsigned i = 0; i<rows; i++){
        for(unsigned j = 0; j<cols; j++){
            std::cout << matrix[i][j] << ' '; 
        }
        std::cout << '\n';
    }
}


std::ostream& operator<< (std::ostream& os, Matrix& matrix){
    
    for(unsigned i = 0; i<matrix.getRows(); i++){
        for(unsigned j = 0; j<matrix.getCols(); j++){
            os << matrix.getValue(i,j);
        }
        os << std::endl;
    }
    return os;
}