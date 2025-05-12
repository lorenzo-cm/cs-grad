#include "menu.hpp"

/**
 * @brief Construct a new Menu:: Menu object
 * 
 * @param database the database used
 */
Menu::Menu(Database database){
    db = database;
    mailbox = new Mailbox(database);
    login = new LoginManager(database);
}

/**
 * @brief Destroy the Menu:: Menu object and its atributes
 * 
 */
Menu::~Menu(){
    if(user != nullptr) delete user;
    if(matcher != nullptr) delete matcher;
    if(mailbox != nullptr) delete mailbox;
    if(mailbox != nullptr) delete login;
}

/**
 * @brief checks if user is logged to decide which menu to show (on main)
 * 
 * @return true if logged
 * @return false if not logged
 */
bool Menu::isLogged(){
    return logged;
}

/**
 * @brief Shows login menu and takes input from user 
 * 
 */
void Menu::showLoginMenu(){
    int choice;
    system("clear||cls");
    std::cout << BHRED <<"FINDER" << reset << std::endl;
    std::cout << "1- Criar conta  2- Fazer Login  3- Sair" << std::endl;
    std::cin >> choice;
    if (std::cin.fail() || choice > 3 || choice < 1){
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        throw invalidNumber();
    }
    switch (choice){
        case 1:{
            registerUser();
            logged = true;
            break;
        }
        case 2:{
            loginUser();
            logged = true;
            break;
        }
        case 3:{
            if(user != nullptr) delete user;
            if(matcher != nullptr) delete matcher;
            if(mailbox != nullptr) delete mailbox;
            if(login != nullptr) delete login;
            
            system("exit");
            exit(0);
            break;
        }
        default:{
            throw invalidNumber();
            break;
        }    
    }
}

/**
 * @brief Shows main menu and takes input from user
 * 
 */
void Menu::showMainMenu(){
    int choice;
    system("clear||cls");
    std::cout << RED << "1- Gerar match   " << reset << "\n2- Mostrar lista de amigos  " << "\n3- Mudar senha  " << "\n4- Deletar conta  "  << "\n5- Redefinir preferências  "<< "\n6- Redefinir características  " << MAG << "\n7- Sair" << reset << "\n\n";
    std::cin >> choice;
    switch (choice){
        case 1:{
            generateMatch();
            break;
        }
        case 2:{
            std::cout << "\n";
            showFriendsList();
            break;
        }
        case 3:{
            std::string oldpass;
            std::string newpass;
            system("clear||cls");
            std::cout << BHBLU << "Digite sua senha atual: " << reset;
            std::cin >> oldpass;
            system("clear||cls");
            std::cout << BHBLU << "Digite sua senha nova: " << reset;
            std::cin >> newpass;
            login->resetPassword(user->getUsername(), oldpass, newpass);
            system("clear||cls");
            std::cout << BHGRN << "Senha alterada com sucesso" << reset << std::endl;
            std::cout << "Pressione enter para continuar ";
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            break;
        }  
        case 4:{
            std::string pass;
            system("clear||cls");
            std::cout << BHRED << "Pressione 0 para sair ou digite sua senha para confirmar: " << reset;
            std::cin >> pass;
            if(pass == to_string(0)) break;
            if(login->deleteAccount(user->getId(), pass)){
                std::cout << BHGRN << "Sua conta foi deletada com sucesso. Esperamos lhe ver de volta em breve :)\n" << reset;
                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                user = nullptr;
                logged = false;
            }
            break;
        }
        case 5:{
            std::vector<int> prefs = setPreferences();
            db.alterPreferencesDatabase(prefs, user->getId());
            break;
        }
        case 6:{
            std::vector<int> chars = setCharacteristics();
            db.alterCharacteristicsDatabase(chars, user->getId());
            break;
        }
        case 7:{
            delete user;
            user = nullptr;
            logged = false;
            break;
        }
        default:{
            throw invalidNumber();
            std::cin.ignore(numeric_limits<streamsize>::max(), '\n');
            break;
        }
    }
}

/**
 * @brief Registers user in database
 * 
 */
void Menu::registerUser(){
    std::string username, name, password, email;
    int age;
    int gender;
    system("clear||cls");
    std::cout << "Digite seu nome de usuário: ";
    std::cin >> username;
    while (db.verifyUserDatabase(username)){
        system("clear||cls");
        std::cout << "Nome de usuário não disponível, tente novamente: ";
        std::cin >> username;
    }
    system("clear||cls");
    std::cout << "Digite seu nome: ";
    std::cin.clear();
    std::cin.ignore(numeric_limits<streamsize>::max(), '\n');
    std::getline (std::cin, name);
    system("clear||cls");
    std::cout << "Digite sua senha: ";
    std::cin >> password;
    if(password == to_string(0)) throw invalidPassword();
    system("clear||cls");
    std::cout << "Digite seu email: ";
    std::cin >> email;
    system("clear||cls");
    std::cout << "Digite sua idade: ";
    std::cin >> age;
    if (std::cin.fail() || age <= 13){
        std::cin.clear();
        cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        throw invalidAge();
    }
    system("clear||cls");
    std::cout << "Digite seu sexo (Feminino = 1 / Masculino = 0): ";
    std::cin >> gender;
    if (std::cin.fail() || (gender != 0 && gender != 1)){
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        throw invalidGender();
    }
    system("clear||cls");
    std::vector<int> prefs = setPreferences();
    std::vector<int> chars = setCharacteristics();
    login->signUP(username, name, password, email, age, gender);
    user = new User(username);
    db.setCharacteristicsDatabase(chars, user->getId());
    db.setPreferencesDatabase(prefs[0], prefs[1], prefs[2], user->getId());
    std::cout << "Usuário registrado com sucesso" << std::endl;
}

/**
 * @brief akes username and password input from user and sets logged to true
 * 
 */
void Menu::loginUser(){
    std::string username, password;
    system("clear||cls");
    std::cout << "Digite seu nome de usuário: ";
    std::cin >> username;
    system("clear||cls");
    std::cout << "Digite sua senha: ";
    std::cin >> password;

    login->login(username, password);
    user = new User(username);
    system("clear||cls");
    std::cout << "Bem vindo, " << username << '.' << std::endl;
    std::cout << "Pressione enter para continuar ";
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

/**
 * @brief Takes input from user and returns vector with characteristics
 * 
 * @return std::vector<int> of characteristics
 */
std::vector<int> Menu::setCharacteristics(){
    std::string characteristics[10] = {"racional", "espirituoso", "divertido", "extrovertido", "ambicioso", "artistico", "esportivo", "gamer", "ativista", "ecológico"};
    std::vector<int> chars;
    system("clear||cls");
    std::cout << "Agora faremos algumas perguntas sobre você!" << std::endl;
    std::cout << "Pressione enter para continuar ";
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    for(int i = 0; i < 10; i++){
        int pref;
        system("clear||cls");
        std::cout << "De 1 a 10, o quanto você se considera " << characteristics[i] << "? ";
        std::cin >> pref;
        if (std::cin.fail() || pref < 1 || pref > 10){
            std::cin.clear();
            std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            throw invalidNumber();
        }
        chars.push_back(pref);
    }
    return chars;
}

/**
 * @brief Takes input from user and returns vector with preferences
 * 
 * @return std::vector<int> of preferences
 */
std::vector<int> Menu::setPreferences(){
    std::vector<int> prefs;
    system("clear||cls");
    std::cout << "Conte-nos um pouco sobre suas preferências." << std::endl;
    std::cout << "Qual é a idade mínima de quem você quer encontrar? ";

    int pref = 0;
    std::cin >> pref;
    prefs.push_back(pref);

    if (std::cin.fail() || prefs[0] < 14 || prefs[0] > 70){
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        throw invalidAge();
    }
    system("clear||cls");
    std::cout << "Qual é a idade máxima de quem você quer encontrar?: ";
    std::cin >> pref;
    prefs.push_back(pref);
    if (std::cin.fail() || prefs[1] < prefs[0]){
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        throw invalidAge();
    }
    system("clear||cls");
    std::cout << "Qual é o sexo de quem você quer encontrar? (Feminino = 1 / Masculino = 0): ";
    std::cin >> pref;
    prefs.push_back(pref);
    if (std::cin.fail() || prefs[2] < 0 || prefs[2] > 1){
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        throw invalidGender();
    }
    return prefs;
}

/**
 * @brief Sends a message to receiver whose username is passed
 * 
 * @param usernameReceiver a string containg the username of whom user wants to send the message to
 */
void Menu::sendMessage(std::string usernameReceiver){
    std::string message;
    system("clear||cls");
    std::cout << "\nDigite sua mensagem: ";
    std::cin.clear();
    std::cin.ignore(numeric_limits<streamsize>::max(), '\n');
    std::getline(std::cin, message);
    mailbox->sendMessage(message, user->getId(), usernameReceiver);
}

/**
 * @brief Shows three most compatible users and adds one as a friend
 * 
 */
void Menu::generateMatch(){
    matcher = new MatchGenerator(user->getId());
    std::vector<int> matches = matcher->match();
    delete matcher;
    matcher = nullptr;


    if(matches.size() == 0) throw matchException();

    int choice;
    system("clear||cls");
    std::cout << "Essas são as pessoas com maior afinidade, escolha uma para adicionar à lista de amigos" << std::endl;
    for(int i = 0; i<matches.size(); i++){
        std::cout << BHWHT << "\n" << i+1<< ": " << db.getUsernameByIdDatabase(matches[i]) << "  ";
    }
    std::cout << "\n\n";

    std::cout << RED << "Se não quiser nenhuma dessas pessoas, digite 0. \n" << reset;
    std::cin >> choice;
    if(choice == 0) return; 
    if (std::cin.fail() || choice > matches.size() || choice < 1){
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        throw invalidNumber();
    }
    db.setFriendsDatabase(user->getId(), matches[choice - 1]);
    db.setFriendsDatabase(matches[choice - 1], user->getId());
    std::cout << db.getUsernameByIdDatabase(matches[choice - 1]) << " adicionado à lista de amigos" << std::endl;
}

/**
 * @brief Shows friends list and gives user the option to chat with them of to go back to the menu
 * 
 */
void Menu::showFriendsList(){
    system("clear||cls");
    std::vector<string> friends = db.getFriendsByIdDatabase(user->getId());
    for(int i = 0; i < friends.size(); i++){
            std::cout << BHWHT << i+1 << "- " << friends[i] << std::endl;
        }
    std::cout << WHT << "\nDigite o número correspondente ao amigo para conversar. \nDigite 0 para voltar.\n "<< reset << std::endl;
    int choice;
    std::cin >> choice;
    system("clear||cls");
    if (std::cin.fail() || choice < 0 || choice > friends.size()){
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        throw invalidGender();
    }
    if(choice > 0){
        showChat(friends[choice-1]);
    }
    if(choice == 0){
        return;
    }
}

/**
 * @brief Shows chat between user and previously choosen friend

 * 
 * @param usernameReceiver a string containg the username of whom user wants to see their chat with
 */
void Menu::showChat(std::string usernameReceiver){
    for(auto message : mailbox->readMessages(user->getId(), usernameReceiver)){
        std::cout << message << std::endl;
    }
    std::cout << BHMAG << "\n1- Enviar mensagem  2- Fechar conversa " << reset << std::endl;
    int isDmOpen;
    std::cin >> isDmOpen;
    system("clear||cls");
    if (std::cin.fail() || isDmOpen < 0 || isDmOpen > 2){
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        throw invalidNumber();
    }
    if(isDmOpen == 1){
        sendMessage(usernameReceiver);
        showChat(usernameReceiver);
    }
}