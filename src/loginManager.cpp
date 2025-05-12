#include "../include/loginManager.hpp"

/**
 * @brief logs in a username with parameters received from the menu.
 * 
 * @param username 
 * @param password 
 * 
 * @return true if logged in successfully. 
 * @throw userNotFound() if user sent by menu doens't exist on the database.
 * @throw invalidPassword() if user exists but password doesn't match with the database's one.
 */
bool LoginManager::login(string username, string password){
    int userID = this->_database.getIdDatabase(username);
    if(userID != INVALIDUSER){
        if(this->checkPassword(userID, password)){
            return true;
        }else{
            throw invalidPassword();
        } 
    }else{
        throw userNotFound();
    }
    return false;
}

/**
 * @brief signs the user up if it doesn't exist on the database yet and logs it in.
 * 
 * @param username 
 * @param name 
 * @param password 
 * @param email 
 * @param age 
 * @param gender 
 * 
 * @return true if user is created successfully.
 * @throw usernameAlreadyInUse() if username sent by menu is already taken.
 * @throw createUserError() if user cannot login after being created.
 */
bool LoginManager::signUP(string username, string name, string password, string email, int age,  int gender){

    int userID = this->_database.getIdDatabase(username);
    if(userID != INVALIDUSER){
        throw usernameAlreadyInUse();
    }
    this->_database.createUserDatabase(username, name, password, email, age, gender);
    int logged = this->login(username, password);
    if(logged){
        return true;
    }else{
        throw createUserError();
    }
    return false;
}
/**
 * @brief checks if password given as parameter and it's user id matches on the database. 
 * 
 * @param userID 
 * @param password 
 * 
 * @return true if password matches.
 * @return false if password doens't match. 
 */
bool LoginManager::checkPassword(int userID, string password){
    string userPassword = this->_database.getPasswordDatabase(userID);
    if(password == userPassword){
        return true;
    }else{
        return false;
    }
}
/**
 * @brief resets the user password if he inputs his old password right. 
 * 
 * @param username 
 * @param oldPassword actual password.
 * @param newPassword desired new password. 
 * 
 * @return true if all rules are followed and password is reset sucessfully.
 * @throw invalidPassword() if the password on the database doesn't match the input from the user.
 * @throw userNotFound() if user desired to change password doesn't exist on the database. 
 */
int LoginManager::resetPassword(string username, string oldPassword, string newPassword){
    int userID = this->_database.getIdDatabase(username);
    if(userID != INVALIDUSER){
        if(this->checkPassword(userID, oldPassword)){
            this->_database.changePasswordDatabase(newPassword, userID);
            return true;
        }else{
            throw invalidPassword();
        } 
    }else{
        throw userNotFound();
    }
    return 0;
}

/**
 * @brief deletes user account after checking his identity by his password. 
 * 
 * @param userID 
 * @param password 
 * 
 * @return true if user is successfully deleted on the database.
 * @throw invalidPassword() if user inputs a wrong password on his identity verification.
 */

bool LoginManager::deleteAccount(int userID, string password){
    if(this->checkPassword(userID, password)){
        this->_database.deleteUserDatabase(userID);
        return true;
    }else{
        throw invalidPassword();
    }
    return false;
}