#include "../include/pca.hpp"
#include <iostream>
using namespace Eigen;

/**
 * @brief makes the z-normalization to a given matrix
 * 
 * @param mat a matrix
 * 
 * @return returns a z-normalized matrix
*/
MatrixXd Pca::zNormalization(MatrixXd& mat){
    MatrixXd m = mat.transpose();
    MatrixXd X_centered = m.colwise() - m.rowwise().mean();
    
    MatrixXd X_var = X_centered;
    for(int i = 0; i<X_centered.rows(); i++){
        for(int j = 0; j<X_centered.cols(); j++){
            X_var(i,j) = X_centered(i,j) * X_centered(i,j);
        }
    }

    X_var = X_var/(X_var.cols()-1);
    MatrixXd var = X_var.rowwise().sum();
    
    MatrixXd std_dev = var;
    for(int i = 0; i<var.rows();i++){
        std_dev(i) = sqrt(var(i));
    }

    MatrixXd X_normalized = X_centered;

    for(int i = 0; i<X_centered.rows();i++){
        for(int j = 0; j<X_centered.cols();j++){
            X_normalized(i,j) = X_centered(i, j)/std_dev(i);
        }
    }
    return X_normalized;
}


/**
 * @brief calculates the covariance matrix of a given matrix
 * 
 * @param zmat a z-normalized matrix
 * 
 * @return returns the covariance matrix
 */
MatrixXd Pca::covMatrix(MatrixXd& zmat){
    return zmat * zmat.transpose();
}


/**
* @brief calculates the pca of
*
* @param zmat a z-normalized matrix
* @param zCX a z-normalized covariance matrix
*
* @return the full pca matrix
*/
MatrixXd Pca::pca_calc(MatrixXd& zmat, MatrixXd& zCX){
    SelfAdjointEigenSolver<MatrixXd> E(zCX);

    MatrixXd eigt = E.eigenvectors().transpose();

    // sort decresingly
    VectorXd aux;
    int rows = eigt.rows();
    for(int i = 0; i<rows/2;i++){
        aux = eigt.row(rows-1 -i);
        eigt.row(rows-1-i) = eigt.row(i);
        eigt.row(i) = (aux);
        
    }

    return eigt * zmat;
}


/**
* @brief calculates the pca of the X matrix
*
* @param X matrix
*
* @return the full pca matrix
*/
MatrixXd Pca::pca(MatrixXd& X){
    MatrixXd zNormX = zNormalization(X);
    MatrixXd covX = covMatrix(zNormX);
    MatrixXd Y = pca_calc(zNormX, covX);
    return Y;
}