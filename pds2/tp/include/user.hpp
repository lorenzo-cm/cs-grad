#ifndef USER_H
#define USER_H

#include "database.hpp"

#include <vector>
#include <string>

class User{
    private:
        Database* database;
        std::string _username;
        int _id;

    public:
        User(std::string username); 			
        int getId();		
        std::string getUsername(); 
        std::vector<int> getPreferences();				
};

#endif
