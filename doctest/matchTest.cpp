#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include "matchGenerator.hpp"

using namespace std;

TEST_CASE("MatchTeste 01 - PCA "){
    Pca pca;
    MatrixXd a(2,2);
    a << 1,3,-2,5;
    MatrixXd result = pca.pca(a);
    MatrixXd b(2,2);
    b<< 1, -1, round(-2.23711432e-17), round(2.23711432e-17);

    CHECK(result == b);
}

TEST_CASE("MatchTeste 02 - match"){
    MatchGenerator mg(10);

    vector<int> a = mg.match();
    vector<int> b {35,40};

    CHECK(a == b);
}

TEST_CASE("MatchTeste 03 - match2"){
    MatchGenerator mg(49);
    CHECK_THROWS_AS(mg.match(), matchException);
}

TEST_CASE("MatchTeste 04 - match3"){
    MatchGenerator mg(13);

    vector<int> a {44};

    CHECK(mg.match() == a);
}

TEST_CASE("MatchTeste 05 - match4"){
    MatchGenerator mg(21);

    vector<int> a {45,30,25};

    CHECK(mg.match() == a);
}