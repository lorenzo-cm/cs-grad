#ifndef LOGIN_MANAGER_H
#define LOGIN_MANAGER_H

#include<iostream>

#include "database.hpp"
#include "exception.hpp"

using namespace std;

class LoginManager{
    private:
        Database _database;
        const int INVALIDUSER = -1;
    public:

        LoginManager(Database database) : _database(database){};
        
        bool login(string username, string password); //if password and login matches, return true

        bool signUP(string username, string name, string password, string email, int age,  int gender); //returns true if user created and logged in successfully

        bool checkPassword(int userID, string password); //returns true if the password given as parameter matches the database's one

        int resetPassword(string username, string oldPassword, string newPassword); //verify permission to change the password to a new value

        bool deleteAccount(int userID, string password);
};

#endif