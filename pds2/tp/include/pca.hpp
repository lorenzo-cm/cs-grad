#ifndef PCA_H
#define PCA_H

#include "eigen/Eigen/Dense"
#include "eigen/Eigen/Eigenvalues"
#include <cmath>

using namespace Eigen;

class Pca{

public:

    MatrixXd zNormalization(MatrixXd& mat);

    MatrixXd covMatrix(MatrixXd& zmat);

    MatrixXd pca_calc(MatrixXd& zmat, MatrixXd& zCX);

    MatrixXd pca(MatrixXd& X);

};


#endif
