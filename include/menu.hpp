#ifndef MENU_H
#define MENU_H

#include "mailbox.hpp"
#include "user.hpp"
#include "loginManager.hpp"
#include "exception.hpp"
#include "matchGenerator.hpp"
#include "colors.hpp"

#include <iostream>
#include <string>
#include <stdlib.h>
#include <limits>


class Menu{
    private:
        bool logged = false;
        Database db;
        User* user = nullptr;
        Mailbox* mailbox = nullptr;
        MatchGenerator* matcher = nullptr;
        LoginManager* login = nullptr;

    public:
        Menu(Database database);
        ~Menu();
        bool isLogged();
        void registerUser(); 
        void loginUser();
        std::vector<int> setCharacteristics(); 
        std::vector<int> setPreferences(); 
        void showLoginMenu(); 
        void showMainMenu(); 
        void sendMessage(std::string receiver); 
        void generateMatch(); 
        void showFriendsList(); 
        void showChat(std::string receiver);
};


#endif