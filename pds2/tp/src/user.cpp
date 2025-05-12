#include "../include/user.hpp"

/**
 * @brief Constructor with username
 * 
 * @param username user username
*/
User::User(std::string username){
    _id = database->getIdDatabase(username);
    _username = username;
}

/**
 * @brief returns user id
 *  
 * @return int, user id
 */
int User::getId(){
    return _id;
}

/**
 * @brief returns username, a string
 * 
 * @return std::string username
 */
std::string User::getUsername(){
    return _username;
}

/**
 * @brief gets user preferences from database returns them
 * 
 * @return std::vector<int> a with user preferences
 */
std::vector<int> User::getPreferences(){
    return database->getPreferencesByIdDatabase(_id);
}

