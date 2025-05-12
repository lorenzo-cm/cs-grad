#ifndef DATABASE_H
#define DATABASE_H

#include "databaseController.hpp"
#include <vector>
#include <iostream>
#include <sstream>


class Database : public DatabaseController
{
    public:
    Database();
    Database(const char* dbName);
    virtual ~Database() override;

    // Sets
    int createUserDatabase(std::string username, std::string name, std::string password, std::string email, int age, int gender, const char* db = _dbName);
    int insertMessageDatabase(std::string message, int idSender, int idReceiver, const char* db = _dbName);
    int changePasswordDatabase(std::string newPassword, int id, const char* db = _dbName);
    int deleteUserDatabase(int id, const char* db = _dbName);
    int setCharacteristicsDatabase(std::vector<int> preferences, int id, const char* db = _dbName);
    int setFriendsDatabase(int id1, int id2, const char* db = _dbName);
    int setPreferencesDatabase(int minAge, int maxAge, int gender, int id, const char* db = _dbName);
    int alterPreferencesDatabase(std::vector<int>newValues, int id, const char* db = _dbName);
    int alterCharacteristicsDatabase(std::vector<int>newValues, int id, const char* db = _dbName);

    // Gets
    std::string getPasswordDatabase(int id, const char* db = _dbName);
    int getIdDatabase(std::string username, const char* db = _dbName);
    bool verifyUserDatabase(std::string username, const char* db = _dbName);
    bool verifyFriendshipDatabase(int friendid, int id, const char* db = _dbName);
    std::string getUsernameByIdDatabase(int id, const char* db = _dbName);
    std::vector<int> getPreferencesByIdDatabase(int id, const char* db = _dbName);
    std::vector<int> getMatchedPeoplePreferencesIdDatabase(std::vector<int> preferences, const char* db = _dbName); 
    std::vector<std::string> getMessagesBetweenIdsDatabase(int id1, int id2, const char* db = _dbName);
    std::vector<std::string> getFriendsByIdDatabase(int id, const char* db = _dbName);
    std::vector<std::vector<double>> getCharacteristicsDatabase(std::vector<int> ids, const char* db = _dbName);
    std::vector<int> getCharacteristicsByIdDatabase(int id, const char* db = _dbName);
    std::vector<int> getMatchCompatibleIds(int id, const char* db = _dbName);
    std::vector<int> getInfoById(int id, const char* db = _dbName);

    // example
    std::vector<std::string> selectVectorString(std::string command, const char* db = _dbName);
};

#endif