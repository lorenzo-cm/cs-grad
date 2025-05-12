#ifndef DATABASECONTROLLER_H
#define DATABASECONTROLLER_H

#include <iostream>
#include <iomanip>
#include <sqlite3.h>


class DatabaseController{
    protected:

        static const char* _dbName;
        // it needs to be static
        static int callback(void* p, int argc, char** argv, char** colName);
        static int first;

    public:
        DatabaseController();
        DatabaseController(const char* dbName);
        virtual ~DatabaseController();
        
        int select(std::string command, const char* db = _dbName);
        int command(std::string command, const char* db = _dbName);
};

#endif
