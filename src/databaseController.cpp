#include "databaseController.hpp"

using namespace std;

int DatabaseController::first = 0;
const char* DatabaseController::_dbName = "";


DatabaseController::DatabaseController(){}


/**
 * @brief Constructor with database name
 * 
 * @param dbName name of the database
*/
DatabaseController::DatabaseController(const char* dbName){
	_dbName = dbName;
}


DatabaseController::~DatabaseController(){}

/**
 * @brief Function to make commands in the database
 * 
 * @param command the sql query
 * @param db the database that will be requested
 * 
 * @return 0 if sucessful and 1 otherwise
*/
int DatabaseController::command(std::string command, const char* db){
	sqlite3* DB;
	char* messageError;

	int exit = sqlite3_open(db, &DB);

	exit = sqlite3_exec(DB, command.c_str(), NULL, NULL, &messageError);

	if (exit != SQLITE_OK) {
		sqlite3_close(DB);
        cerr << messageError << endl;
		return 1;
	}

	sqlite3_free(messageError);
	sqlite3_close(DB);
	return 0;
}


/**
 * @brief A callback is a function passed as an argument to another function, this function is passed as parameter in Database::Select and is used to print the fields
 * 
 * @param p_data pointer to data in the 4th argument of sqlite3_exec()
 * @param numFields the number of columns, an int
 * @param pFields an array of strings representing the data inside the columns
 * @param colName an array of strings representing column names
 * 
 * @return 0 if sucessful and 1 otherwise
*/
int DatabaseController::callback(void* p_data, int numFields, char** pFields, char** colName)
{
	if(first == 0){
		for (int i = 0; i < numFields; i++) {
			cout << setw(10) << colName[i] << ' ';
		}
		cout << '\n';
	}

    for (int i = 0; i < numFields; i++) {
		cout << setw(10) << pFields[i] << ' ';
	}
	cout << "\n";

	first++;

	return 0;
}


/**
 * @brief Function to make the SELECT statement in SQL and print it with the callback function
 * 
 * @param command the sql query, a string
 * @param db the database that will be requested
 * 
 * @return 0 if sucessful and 1 otherwise
*/
int DatabaseController::select(std::string command,  const char* db){
	this->first = 0;
    sqlite3* DB;
	char* messageError;

	int exit = sqlite3_open(db, &DB);

	/* An open database, SQL to be evaluated, Callback function, 1st argument to callback, Error msg written here*/
	exit = sqlite3_exec(DB, command.c_str(), callback, NULL, &messageError);

	if (exit != SQLITE_OK) {
		sqlite3_close(DB);
        cerr << messageError << endl;
		return 1;
	}

	this->first = 0;
	sqlite3_free(messageError);	
	sqlite3_close(DB);
	cout << '\n';
	return 0;
}