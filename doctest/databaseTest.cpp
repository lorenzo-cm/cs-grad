#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include "database.hpp"

TEST_CASE("DatabaseTest 01 - Verify User"){
    Database database("database.db");
    bool added = database.verifyUserDatabase("tomaslm00");
    CHECK(added);
}

TEST_CASE("DatabaseTest 02 - Verify friendship"){
    Database database("database.db");
    bool added = database.verifyFriendshipDatabase(41, 16);
    CHECK(added);
}

TEST_CASE("DatabaseTest 03 - Get Id function"){
    Database database("database.db");
    int id = database.getIdDatabase("tomaslm00");
    bool added;
    if(id == 1)
    {
        added = true;   
    }
    else
    {
        added = false;
    } 
    CHECK(added);
}

TEST_CASE("DatabaseTest 04 - Get username by id function"){
    Database database("database.db");
    std::string username = database.getUsernameByIdDatabase(41);
    bool added;
    if(username == "tomaslm00")
    {
        added = true;   
    }
    else
    {
        added = false;
    } 
    CHECK(added);
}


TEST_CASE("DatabaseTest 05 - get Password Database"){
    Database database("database.db");
    std::string password = database.getPasswordDatabase(41);
    bool added;
    if(password == "tomasmuniz14")
    {
        added = true;   
    }
    else
    {
        added = false;
    } 
    CHECK(added);
}