#include "menu.hpp"

using namespace std;

int main()
{
   Database database("database.db");
   Menu menu(database);

   while(1){
    try{
        if(menu.isLogged()){
        menu.showMainMenu();
        }else{
        menu.showLoginMenu();
        }
    }catch(Exception& e){
        cerr << ITRED;
        e.what();
        cerr << reset;
        string buffer;
        getline(cin, buffer);
        cin.ignore();
    }
   }
   return 0;
}
