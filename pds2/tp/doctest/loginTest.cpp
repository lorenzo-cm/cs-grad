#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include "../include/menu.hpp"

TEST_CASE("LoginTest 01 - Tests if user can sign up"){
    Database database("database.db");
    LoginManager login(database);
    bool added = login.signUP("TesteAutomatizado", "Teste", "SenhaTeste", "email@teste.com", 20, 1);
    CHECK(added);
}

TEST_CASE("LoginTest 02 - Tests if user can login in ideal scenario"){
    Database database("database.db");
    LoginManager login(database);
    bool logged  = login.login("TesteAutomatizado", "SenhaTeste");
    CHECK(logged);
}

TEST_CASE("LoginTest 03/1 - Tests if user can change his password in ideal scenario"){
    Database database("database.db");
    LoginManager login(database);
    bool passwordReset = login.resetPassword("TesteAutomatizado", "SenhaTeste", "senhaNova");
    CHECK(passwordReset);
}

TEST_CASE("LoginTest 03/2 - Tests if user can change his password in ideal scenario reverse"){
    Database database("database.db");
    LoginManager login(database);
    bool passwordReset = login.resetPassword("TesteAutomatizado", "senhaNova", "SenhaTeste");
    CHECK(passwordReset);
}

TEST_CASE("LoginTest 04 - Tests if real user can login with wrong password"){
    Database database("database.db");
    LoginManager login(database);
    CHECK_THROWS_AS(login.login("TesteAutomatizado", "RandomPassword"), invalidPassword);
}

TEST_CASE("LoginTest 05 - Tests if fake user can login"){
    Database database("database.db");
    LoginManager login(database);
    CHECK_THROWS_AS(login.login("RandomUser", "SenhaTeste"), userNotFound);
}

TEST_CASE("LoginTest 06 - Tests if new user can reuse a taken username"){
    Database database("database.db");
    LoginManager login(database);
    CHECK_THROWS_AS(bool added = login.signUP("TesteAutomatizado", "Teste", "SenhaTeste", "email@teste.com", 20, 1), usernameAlreadyInUse);
}

TEST_CASE("LoginTest 07 - Tests if password given by user matches database's one"){
    Database database("database.db");
    LoginManager login(database);
    int id = database.getIdDatabase("TesteAutomatizado");
    bool validPassword = login.checkPassword(id, "SenhaTeste");
    CHECK(validPassword);
}

TEST_CASE("LoginTest 08 - Tests if user can change it's own password by inputing a wrong original one"){
    Database database("database.db");
    LoginManager login(database);
    CHECK_THROWS_AS(login.resetPassword("TesteAutomatizado", "RandomPassword", "SenhaTeste"), invalidPassword);
}

TEST_CASE("LoginTest 09 - Tests if user that does not exist can change a password"){
    Database database("database.db");
    LoginManager login(database);
    CHECK_THROWS_AS(login.resetPassword("RandomUser", "RandomPassword", "SenhaTeste"), userNotFound);
}

TEST_CASE("LoginTest 10 - Tests if user can delete his account by giving his wrong password"){
    Database database("database.db");
    LoginManager login(database);
    int id = database.getIdDatabase("TesteAutomatizado");
    CHECK_THROWS_AS(login.deleteAccount(id, "RandomPassword"), invalidPassword);
}



TEST_CASE("LoginTest 11 - Tests if user can delete his account in ideal scenario"){
    Database database("database.db");
    LoginManager login(database);
    int id = database.getIdDatabase("TesteAutomatizado");
    bool deleted = login.deleteAccount(id, "SenhaTeste");
    CHECK(deleted);
}