#ifndef MAILBOX_H
#define MAILBOX_H


#include "database.hpp"
#include "exception.hpp"
#include <vector>
#include <string>
#include <iostream>
#include <algorithm>


class Mailbox{

    private:
        Database database;

    public:

        Mailbox(Database _database) : database(_database){};

        int sendMessage(std::string message, int idSender, std::string usernameReceiver);
    
        std::vector<std::string> readMessages(int idSender, std::string usernameReceiver);

};

#endif
