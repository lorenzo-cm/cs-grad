#ifndef MATCHGENERATOR_H
#define MATCHGENERATOR_H

#include "pca.hpp"
#include "exception.hpp"
#include "database.hpp"

#include <vector>
#include <Eigen/Dense>
#include <algorithm>
#include <cmath>

#define vvd std::vector<std::vector<double>>

class MatchGenerator{
    private:
        int _id;
        int pos;

    public:

        MatchGenerator(int id);

        void sortData(vvd& data);

        std::vector<double> calculatesDistance(vvd& pcaData, int dimensions = 3);

        std::vector<int> match();

        std::vector<std::pair<int, double>> matchAll();

        vvd getCharacteristicsMatrixFiltered();

        vvd matrixToVector(MatrixXd& eMatrix);

        MatrixXd vectorToMatrix(vvd& vMatrix);
        
};


#endif
