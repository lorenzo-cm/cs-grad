#include "../include/mailbox.hpp"


/**
 * @brief Sends message (inserts it into the database) with the username attached
 * 
 * @param message a string cointaning a message
 * @param idSender the user Id, an integer
 * @param usernameReceiver a string containg the username of whom user wants to send the message to
 * 
 * @return 0 if sucessful 
 * @return 1 otherwise
*/
int Mailbox::sendMessage(std::string message, int idSender, std::string usernameReceiver){
    
    int idReceiver = database.getIdDatabase(usernameReceiver);

    //formarting the message
    std::string UsernameSender = database.getUsernameByIdDatabase(idSender);
    std::string Colon = ": ";
    std::string MessageWithName = UsernameSender + Colon + message;

    if(idReceiver == -1){
        throw userNotFound();
    }

    
    //inserting message into the database
    if(this->database.insertMessageDatabase(MessageWithName, idSender, idReceiver) == 0){
        return 0;

    } else{
        throw sendMessageError();
        return 1;
    }


}
    

/**
 * @brief Gets a vector from the database cointaining all the messages between user and a friend 
 * 
 * @param idSender the user Id, an integer
 * @param usernameReceiver a string containg the username of whom user wants to see their chat with
 * 
 * @return the vector in chronological order
*/
std::vector<std::string> Mailbox::readMessages(int idSender, std::string usernameReceiver){
    
    int idReceiver = database.getIdDatabase(usernameReceiver);
    
    //next lines check if said username is id's friend, if not, it can't message them
    std::vector<std::string> friends = this->database.getFriendsByIdDatabase(idSender);
    bool isFriend = false;

    for(auto i : friends){
        if(i == usernameReceiver){
            isFriend = true;
        }
    }

    if(!isFriend){
        throw NotFriend();
    }

    std::vector<std::string> AllMessages = database.getMessagesBetweenIdsDatabase(idSender, idReceiver);

    if(AllMessages.empty()){
        cout << "Você ainda não possui mensagens com esse amigo :/" << endl;
    }

    reverse(AllMessages.begin(), AllMessages.end());
    
    return AllMessages;

}
