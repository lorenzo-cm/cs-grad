#include "database.hpp"

std::vector<int> findCommonIds(std::vector<int> vec1, std::vector<int> vec2);

Database::Database(){}

Database::Database(const char* dbName) : DatabaseController(dbName){}

Database::~Database(){}

// Gets



/**
 * @brief verify if a person is friends with another person
 * @param friendid integer
 * @param id integer
 * @return returns false if it isnt returns true if it is
*/
bool Database::verifyFriendshipDatabase(int friendid, int id, const char* db)
{
    std::string command = "SELECT userid FROM friends WHERE friendId = ? AND userid = ?";

    sqlite3* DB;
    int idFromDb = -1;

    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);

	if (exit != SQLITE_OK) {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return false;
	}
    else
    {
        sqlite3_bind_int(mat, 1, friendid);
        sqlite3_bind_int(mat, 2, id);
    }
	while((exit = sqlite3_step(mat)) == SQLITE_ROW){
		idFromDb = sqlite3_column_int(mat, 0);
	}
	sqlite3_finalize(mat);
	sqlite3_close(DB);
    if(idFromDb > 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}



/**
 * @brief queries the database for all the characteristics of a given id
 * 
 * @param id an integer
 * 
 * @return returns a vector of integers containing the characteristics
*/
std::vector<int> Database::getCharacteristicsByIdDatabase(int id, const char* db)
{
    sqlite3* DB;
    std::vector<int> characteristics;
    
    std::string command = "SELECT userid, characteristicValor FROM characteristics WHERE userid = ?";
    
    int exit = sqlite3_open(db, &DB);
    sqlite3_stmt* mat;
    exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
    if (exit != SQLITE_OK) {
        sqlite3_close(DB);
        sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
        return characteristics;
    }
    else
    {
        sqlite3_bind_int(mat, 1, id);
    }
    bool firstIt = true;
    while((exit = sqlite3_step(mat)) == SQLITE_ROW){
        if(firstIt == true)
        {
            double id = double(sqlite3_column_int(mat, 0));
            characteristics.push_back(id);
            firstIt = false;
        }
        double dValue = double(sqlite3_column_int(mat, 1));
        characteristics.push_back(dValue);
    }
    sqlite3_finalize(mat);     
    sqlite3_close(DB);
    return characteristics; 
}



/**
 * @brief queries the database to see if username already exists
 * 
 * @param username a string
 * 
 * @return returns a true if username is already there || false if is not
*/
bool Database::verifyUserDatabase(std::string username, const char* db)
{
    std::string command = "SELECT username FROM users WHERE username = ?";

    sqlite3* DB;
    std::string usernameFromDb;

    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);

	if (exit != SQLITE_OK) {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return false;
	}
    else
    {
        sqlite3_bind_text(mat, 1, username.c_str(), username.length(), SQLITE_TRANSIENT);
    }
	while((exit = sqlite3_step(mat)) == SQLITE_ROW){
		usernameFromDb = std::string((char *) sqlite3_column_text(mat, 0));
	}
	sqlite3_finalize(mat);
	sqlite3_close(DB);
    if(usernameFromDb.empty())
    {
        return false;
    }
    else
    {
        return true;
    }
}





/**
 * @brief queries the database for a password
 * 
 * @param id an integer 
 * 
 * @return returns a string with the password
*/
std::string Database::getPasswordDatabase(int id, const char* db){
   
    std::string command = "SELECT password FROM users WHERE id = ?";

    sqlite3* DB;
    std::string password;

    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);

	if (exit != SQLITE_OK) {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return password;
	}
    else
    {
        sqlite3_bind_int(mat, 1, id);
    }
	while((exit = sqlite3_step(mat)) == SQLITE_ROW){
		password = std::string((char *) sqlite3_column_text(mat, 0));
	}
	sqlite3_finalize(mat);
	sqlite3_close(DB);
	return password;
}


/**
 * @brief queries the database for an Id
 * 
 * @param username a string 
 * 
 * @return returns the id in an integer format;
*/
int Database::getIdDatabase(std::string username, const char* db)
{
    
    std::string command = "SELECT id FROM users WHERE username = ?";

    sqlite3* DB;
    std::stringstream ssId;
    int id = -1;

    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK) {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return id;
	}
    else
    {
        sqlite3_bind_text(mat, 1, username.c_str(), username.length(), SQLITE_TRANSIENT);
    }
	while((exit = sqlite3_step(mat)) == SQLITE_ROW){
		ssId << std::string((char *) sqlite3_column_text(mat, 0));
	}
    ssId >> id;
	sqlite3_finalize(mat);
	sqlite3_close(DB);
	return id;
}

/**
 * @brief queries the database for the users preference table
 * 
 * @param id an integer 
 * 
 * @return returns a vector with the preferences in the given order
 * | minAge -> 0 | maxAge -> 1 | gender -> 2 | userid -> 3
 * */
std::vector<int> Database::getPreferencesByIdDatabase(int id, const char* db){
    
    std::string command = "SELECT * FROM preferences WHERE userid = ?";
    ;

    sqlite3* DB;
    std::vector<int> preferences;

    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK) {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return preferences;
	}
    else
    {
        sqlite3_bind_int(mat, 1, id);
    }
	while((exit = sqlite3_step(mat)) == SQLITE_ROW){
		for(int i = 0; i < 4; i++)
        {
            std::stringstream ssPreferences;
            ssPreferences << std::string((char *) sqlite3_column_text(mat, i));
            int iPreferences;
            ssPreferences >> iPreferences;
            preferences.push_back(iPreferences);
        }
	}
	sqlite3_finalize(mat);
	sqlite3_close(DB);
	return preferences;
}


/**
 * @brief queries the database for every user that fits given preferences
 * 
 * @param preferences a vector of integers representing preferences 
 * 
 * @return returns a vector of ints with the id of every user that fits the description
*/
std::vector<int> Database::getMatchedPeoplePreferencesIdDatabase(std::vector<int> preferences, const char* db)
{
    int minAge = preferences[0], maxAge = preferences[1], gender = preferences[2];
    std::vector<int> agesVec, genderVec;
    std::string command = "SELECT id FROM users WHERE gender = ?";

    sqlite3* DB;
    std::vector<int> ids;

    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK) {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return ids;
	}
    else
    {
        sqlite3_bind_int(mat, 1, gender);
    }
	while((exit = sqlite3_step(mat)) == SQLITE_ROW)
    {	
        int iGender =  sqlite3_column_int(mat, 0);
        genderVec.push_back(iGender);      
	}

    command = "SELECT id FROM users WHERE age > ? AND age < ?";

    exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return ids;
	}
    else
    {
        sqlite3_bind_int(mat, 1, (minAge - 1));
        sqlite3_bind_int(mat, 2, (maxAge + 1));
    }
	while((exit = sqlite3_step(mat)) == SQLITE_ROW)
    { 
        int iAges = sqlite3_column_int(mat, 0);
        agesVec.push_back(iAges);      
	}

    ids = findCommonIds(agesVec, genderVec);


	sqlite3_finalize(mat);
	sqlite3_close(DB);
	return ids;
}


/**
 * @brief queries the database for username
 * 
 * @param id integer id 
 * 
 * @return string containing username
*/
std::string Database::getUsernameByIdDatabase(int id, const char* db)
{
    std::string command = "SELECT username FROM users WHERE id = ?";
    sqlite3* DB;
    std::string username;

    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return username;
	}
    else
    {
        sqlite3_bind_int(mat, 1, id);
    }
	while((exit = sqlite3_step(mat)) == SQLITE_ROW)
    {
		
        username = std::string((char *) sqlite3_column_text(mat, 0));
	}
	sqlite3_finalize(mat);
	sqlite3_close(DB);
	return username;
}


/**
 * @brief queries the database for messages between two users
 * 
 * @param id1 integer
 * @param id2 integer
 * 
 * @return returns a vector of strings containing the last 10 messages orderned in descendant order by time from 2 users
*/
std::vector<std::string> Database::getMessagesBetweenIdsDatabase(int id1, int id2, const char* db)
{
    std::string command = "SELECT message FROM mailBox WHERE senderId = ? AND receiverId = ? OR senderId = ? AND receiverId = ? ORDER BY time DESC LIMIT 10";
    sqlite3* DB;
    std::vector<std::string> messageVector;
    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return messageVector;
	}
    else
    {
        sqlite3_bind_int(mat, 1, id1);
        sqlite3_bind_int(mat, 2, id2);
        sqlite3_bind_int(mat, 3, id2);
        sqlite3_bind_int(mat, 4, id1);
    }
	while((exit = sqlite3_step(mat)) == SQLITE_ROW)
    {
        messageVector.push_back(std::string((char *) sqlite3_column_text(mat, 0)));
	}
	sqlite3_finalize(mat);
	sqlite3_close(DB);
	return messageVector;
}



/**
 * @brief gets all the user's friends names 
 * 
 * @param id integer
 * 
 * @return returns a vector of strings containing a friend name each
*/
std::vector<std::string> Database::getFriendsByIdDatabase(int id, const char* db)
{
    std::string command = "SELECT friendId FROM friends WHERE userid = ?";

    sqlite3* DB;
    std::vector<std::string> friends;
    std::vector<int> friendsId;
    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return friends;
	}
    else
    {
        sqlite3_bind_int(mat, 1, id);
    }
	while((exit = sqlite3_step(mat)) == SQLITE_ROW)
    {
        int iId = sqlite3_column_int(mat, 0);
        friendsId.push_back(iId);
	}

	sqlite3_finalize(mat);

    for(auto i: friendsId)
    {
        friends.push_back(getUsernameByIdDatabase(i));
    }

	sqlite3_close(DB);
	return friends;
}


/**
 * @brief queries database for characteristics of every user that may be a match potential
 * 
 * @param ids vector of integers holding potential matches id's 
 * 
 * @return returns a matrix of doubles holding id on the first column and the characteristics values on the following order
 * Rational | Spiritual | Humorous | Extrovert | Ambitious | Artsy | Sporty | Gamer | Activist | NatureFriendly
*/
std::vector<std::vector<double>> Database::getCharacteristicsDatabase(std::vector<int> ids, const char* db)
{
    sqlite3* DB;
    std::vector<std::vector<double>> characteristicsMatrix;
    
    for(auto i : ids)
    {
        std::string command = "SELECT userid, characteristicValor FROM characteristics WHERE userid = ?";
        std::vector<double> doubleVector;
        doubleVector.clear();
        
        int exit = sqlite3_open(db, &DB);
        sqlite3_stmt* mat;
        exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
        
        if (exit != SQLITE_OK) {
            sqlite3_close(DB);
            sqlite3_finalize(mat);
            std::cerr << "Erro ao selecionar database" << std::endl;
            return characteristicsMatrix;
        }
        else
        {
            sqlite3_bind_int(mat, 1, i);
        }
        bool firstIt = true;
        while((exit = sqlite3_step(mat)) == SQLITE_ROW){
            if(firstIt == true)
            {
                double id = double(sqlite3_column_int(mat, 0));
                doubleVector.push_back(id);
                firstIt = false;
            }
            double dValue = double(sqlite3_column_int(mat, 1));
            doubleVector.push_back(dValue);
        }
        characteristicsMatrix.push_back(doubleVector);
        sqlite3_finalize(mat);    
    }
    sqlite3_close(DB);
    return characteristicsMatrix;
}


/**
 * @brief gets all the possible matches from a person
 * 
 * @param id integer
 * 
 * @return returns a vector of integers containing all the ids of potential matches 
*/
std::vector<int> Database::getMatchCompatibleIds(int id, const char* db)
{
    std::vector<int> preferences = getPreferencesByIdDatabase(id);
    std::vector<int> matchedids = getMatchedPeoplePreferencesIdDatabase(preferences);
    std::vector<int> infoId = getInfoById(id);
    std::vector<int> results;
    results.push_back(id);
    if(matchedids.size() > 0)
    {
        for(auto i : matchedids)
        {
            std::vector<int> mPreferences = getPreferencesByIdDatabase(i);
            bool friends = verifyFriendshipDatabase(i, id);
            if(infoId.at(1) <= mPreferences.at(1) && infoId.at(1) >= mPreferences.at(0) && infoId.at(0) == mPreferences.at(2) && !friends)
            {
                results.push_back(i);
            }
        }
        return results;
    }
    else
    {
        return results;
    }    
    
}

/**
 * @brief gets gender and age from an user
 * 
 * @param id integer
 * 
 * @return vector of integers containing gender and age and gender from preferences
*/
std::vector<int> Database::getInfoById(int id, const char* db)
{
    std::string command = "SELECT gender, age FROM users WHERE id = ?";
    sqlite3* DB;
    std::vector<int> infoVector;
    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return infoVector;
	}
    else
    {
        sqlite3_bind_int(mat, 1, id);
    }
	while((exit = sqlite3_step(mat)) == SQLITE_ROW)
    {
        for(int i = 0; i < 2; i++)
        {
            infoVector.push_back(sqlite3_column_int(mat, i));
        }
	}
	sqlite3_finalize(mat);
	command = "SELECT gender FROM preferences WHERE userid = ?";
    exit = sqlite3_open(db, &DB);
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return infoVector;
	}
    else
    {
        sqlite3_bind_int(mat, 1, id);
    }
	while((exit = sqlite3_step(mat)) == SQLITE_ROW)
    {
        infoVector.push_back(sqlite3_column_int(mat, 0));
	}
	sqlite3_finalize(mat);
    
    
    sqlite3_close(DB);
	return infoVector;
}






// Sets
/**
 * @brief inserts user into database
 * 
 * @param username string
 * @param name string
 * @param password string
 * @param email string
 * @param age int
 * @param gender int 
 * 
 * @return returns 0 for sucess 1 for error
*/
int Database::createUserDatabase(std::string username, std::string name, std::string password, std::string email, int age, int gender, const char* db)
{
    std::string command = "INSERT INTO users(username, name, password, email, age, gender) VALUES (?, ?, ?, ?, ?, ?)";
    
    sqlite3* DB;
    sqlite3_stmt* st;


    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK)
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return 1;
	}
    else
    {
        sqlite3_bind_text(mat, 1, username.c_str(), username.length(), SQLITE_TRANSIENT);
        sqlite3_bind_text(mat, 2, name.c_str(), name.length(), SQLITE_TRANSIENT);
        sqlite3_bind_text(mat, 3, password.c_str(), password.length(), SQLITE_TRANSIENT);
        sqlite3_bind_text(mat, 4, email.c_str(), email.length(), SQLITE_TRANSIENT);
        sqlite3_bind_int(mat, 5, age);
        sqlite3_bind_int(mat, 6, gender);
        sqlite3_step(mat);
    }

    sqlite3_finalize(mat);
	sqlite3_close(DB);
	return 0;

}



/**
 * @brief inserts message into database
 * 
 * @param message string
 * @param idSender integer
 * @param idReceiver integer
 * 
 * @return returns 0 for sucess 1 for error
*/
int Database::insertMessageDatabase(std::string message, int idSender, int idReceiver, const char* db)
{
    sqlite3* DB;

    std::string command = "INSERT INTO mailBox(message, senderId, receiverId, time) VALUES (? , ? , ? , (SELECT datetime('now')))";
    sqlite3_stmt* st;


    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return 1;
	}
    else
    {
        sqlite3_bind_text(mat, 1, message.c_str(), message.length(), SQLITE_TRANSIENT);
        sqlite3_bind_int(mat, 2, idSender);
        sqlite3_bind_int(mat, 3, idReceiver);
        sqlite3_step(mat);
    }

    sqlite3_finalize(mat);
	sqlite3_close(DB);
	return 0;
}

/**
 * @brief updates password value in database
 * 
 * @param newPassword string
 * @param idS integer
 * 
 * @return returns 0 for sucess 1 for error
*/
int Database::changePasswordDatabase(std::string newPassword, int id, const char* db)
{
    sqlite3* DB;

    std::string command = "UPDATE users SET password = ? WHERE id = ?";
    sqlite3_stmt* st;


    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return 1;
	}
    else
    {
        sqlite3_bind_text(mat, 1, newPassword.c_str(), newPassword.length(), SQLITE_TRANSIENT);
        sqlite3_bind_int(mat, 2, id);
        sqlite3_step(mat);
    }

    sqlite3_finalize(mat);
	sqlite3_close(DB);
	return 0;
}

/**
 * @brief removes user from database
 * 
 * @param id integer
 * 
 * @return returns 0 for sucess 1 for error
*/
int Database::deleteUserDatabase(int id, const char* db)
{
    sqlite3* DB;

    std::string command = "DELETE FROM users WHERE id = ?";
    sqlite3_stmt* st;


    int exit = sqlite3_open(db, &DB);
	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return 1;
	}
    else
    {
        sqlite3_bind_int(mat, 1, id);
        sqlite3_step(mat);
    }

    command = "DELETE FROM friends WHERE userid = ? OR friendId = ?";
    exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return 1;
	}
    else
    {
        sqlite3_bind_int(mat, 1, id);
        sqlite3_bind_int(mat, 2, id);
        sqlite3_step(mat);
    }

    command = "DELETE FROM preferences WHERE userid = ?";
    exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return 1;
	}
    else
    {
        sqlite3_bind_int(mat, 1, id);
        sqlite3_step(mat);
    }

    command = "DELETE FROM mailBox WHERE senderId = ? OR receiverId = ?";
    exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return 1;
	}
    else
    {
        sqlite3_bind_int(mat, 1, id);
        sqlite3_bind_int(mat, 2, id);
        sqlite3_step(mat);
    }

    command = "DELETE FROM characteristics WHERE userid = ?";
    exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
    
	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return 1;
	}
    else
    {
        sqlite3_bind_int(mat, 1, id);
        sqlite3_step(mat);
    }

    sqlite3_finalize(mat);
	sqlite3_close(DB);
	return 0;
}


/**
 * @brief Adds user characteristics to a database
 * 
 * @param id integer
 * @param preferences vector of int representing preferences
 * 
 * @return returns 0 for sucess 1 for error
*/
int Database::setCharacteristicsDatabase(std::vector<int> preferences, int id, const char* db)
{
    sqlite3* DB;
    std::string characteristics[] = {"Rational", "Spiritual", "Humorous", "Extrovert", "Ambitious", "Artsy", "Sporty", "Gamer", "Activist", "NatureFriendly"};
    int iterator = 0;
    for(auto i : preferences)
    {
        std::string command = "INSERT INTO characteristics (userid, characteristic, characteristicValor) VALUES (?, ?, ?)";
        sqlite3_stmt* st;


        int exit = sqlite3_open(db, &DB);
        sqlite3_stmt* mat;
        exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
        
        if (exit != SQLITE_OK) 
        {
            sqlite3_close(DB);
            sqlite3_finalize(mat);
            std::cerr << "Erro ao selecionar database" << std::endl;
            return 1;
        }
        else
        {
            sqlite3_bind_int(mat, 1, id);
            sqlite3_bind_text(mat, 2, characteristics[iterator].c_str(), characteristics[iterator].length(), SQLITE_TRANSIENT);
            sqlite3_bind_int(mat, 3, i);
            sqlite3_step(mat);
        }

        sqlite3_finalize(mat);
        iterator++;
    }
    sqlite3_close(DB);
    return 0;
}



/**
 * @brief Adds a pair of friends to database the first one being the foreign key value
 * 
 * @param id1 integer
 * @param id2 integer
 * 
 * @return returns 0 for sucess 1 for error
*/
int Database::setFriendsDatabase(int id1, int id2, const char* db)
{
    sqlite3* DB;
    std::string command = "INSERT INTO friends (userid, friendId) VALUES (?, ?)";
    sqlite3_stmt* st;


    int exit = sqlite3_open(db, &DB);
    sqlite3_stmt* mat;
    exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
        
    if (exit != SQLITE_OK) 
    {
        sqlite3_close(DB);
        sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
        return 1;
    }
    else
    {
        sqlite3_bind_int(mat, 1, id1);
        sqlite3_bind_int(mat, 2, id2);
        sqlite3_step(mat);
    }

    sqlite3_finalize(mat);
    sqlite3_close(DB);
    return 0;
}


/**
 * @brief Adds user preferences to a database
 * 
 * @param minAge integer
 * @param maxAge integer
 * @param gender integer
 * @param id integer
 * 
 * @return returns 0 for sucess 1 for error
*/
int Database::setPreferencesDatabase(int minAge, int maxAge, int gender, int id, const char* db)
{
    sqlite3* DB;
    std::string command = "INSERT INTO preferences (minAge, maxAge, gender, userid) VALUES (?, ?, ?, ?)";
    sqlite3_stmt* st;


    int exit = sqlite3_open(db, &DB);
    sqlite3_stmt* mat;
    exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
        
    if (exit != SQLITE_OK) 
    {
        sqlite3_close(DB);
        sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
        return 1;
    }
    else
    {
        sqlite3_bind_int(mat, 1, minAge);
        sqlite3_bind_int(mat, 2, maxAge);
        sqlite3_bind_int(mat, 3, gender);
        sqlite3_bind_int(mat, 4, id);
        sqlite3_step(mat);
    }

    sqlite3_finalize(mat);
    sqlite3_close(DB);
    return 0;
}

int Database::alterPreferencesDatabase(std::vector<int> newValues, int id, const char* db)
{
    sqlite3* DB;
    std::string command = "UPDATE preferences SET minAge = ? , maxAge = ?, gender = ? WHERE userid = ?";
    sqlite3_stmt* st;


    int exit = sqlite3_open(db, &DB);
    sqlite3_stmt* mat;
    exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
        
    if (exit != SQLITE_OK) 
    {
        sqlite3_close(DB);
        sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
        return 1;
    }
    else
    {
        sqlite3_bind_int(mat, 1, newValues.at(0));
        sqlite3_bind_int(mat, 2, newValues.at(1));
        sqlite3_bind_int(mat, 3, newValues.at(2));
        sqlite3_bind_int(mat, 4, id);  
        sqlite3_step(mat);
    }

    sqlite3_finalize(mat);
    sqlite3_close(DB);
    return 0;
}

 int Database::alterCharacteristicsDatabase(std::vector<int>newValues, int id, const char* db)
 {
    sqlite3* DB;
    std::string characteristics[] = {"Rational", "Spiritual", "Humorous", "Extrovert", "Ambitious", "Artsy", "Sporty", "Gamer", "Activist", "NatureFriendly"};
    std::string command = "DELETE FROM characteristics WHERE userid = ?";
    sqlite3_stmt* st;


    int exit = sqlite3_open(db, &DB);
    sqlite3_stmt* mat;
    exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
        
    if (exit != SQLITE_OK) 
    {
        sqlite3_close(DB);
        sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
        return 1;
    }
    else
    {
        sqlite3_bind_int(mat, 1, id);
        sqlite3_step(mat);
    }

    sqlite3_finalize(mat);

    int iterator = 0;
    for(auto i : newValues)
    {
        command = "INSERT INTO characteristics (userid, characteristic, characteristicValor) VALUES (?, ?, ?)";
        sqlite3_stmt* st;


        exit = sqlite3_open(db, &DB);
        sqlite3_stmt* mat;
        exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);
        
        if (exit != SQLITE_OK) 
        {
            sqlite3_close(DB);
            sqlite3_finalize(mat);
            std::cerr << "Erro ao selecionar database" << std::endl;
            return 1;
        }
        else
        {
            sqlite3_bind_int(mat, 1, id);
            sqlite3_bind_text(mat, 2, characteristics[iterator].c_str(), characteristics[iterator].length(), SQLITE_TRANSIENT);
            sqlite3_bind_int(mat, 3, i);
            sqlite3_step(mat);
        }

        sqlite3_finalize(mat);
        iterator++;
    }
    sqlite3_close(DB);
    return 0;
 }













std::vector<std::string> Database::selectVectorString(std::string command, const char* db){
    sqlite3* DB;
	std::vector<std::string> vs;

	int exit = sqlite3_open(db, &DB);

	sqlite3_stmt* mat;
	exit = sqlite3_prepare_v2(DB, command.c_str(), -1, &mat, NULL);

	if (exit != SQLITE_OK) 
    {
		sqlite3_close(DB);
		sqlite3_finalize(mat);
        std::cerr << "Erro ao selecionar database" << std::endl;
		return vs;
	}

	
	while((exit = sqlite3_step(mat)) == SQLITE_ROW)
    {
		for(int i = 0; i<7; i++)
        {
			
			vs.push_back(std::string((char *) sqlite3_column_text(mat, i)));
		}
	}

	sqlite3_finalize(mat);
	sqlite3_close(DB);
	return vs;
}


std::vector<int> findCommonIds(std::vector<int> vec1, std::vector<int> vec2)
{
    std::vector<int> aux;
    for(auto i : vec1)
    {
        for(auto j : vec2)
        {
            if(i == j)
            {
                aux.push_back(j);
            }
        }
    }
    return aux;
}