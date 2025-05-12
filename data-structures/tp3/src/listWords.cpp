#include "listWords.hpp"

/**
 * @brief Construct a new List Words:: List Words object
 * 
 */
ListWords::ListWords(){
    head = nullptr;
    tail = nullptr;
    size = 0;
}


/**
 * @brief Destroy the List Words:: List Words object
 * 
 */
ListWords::~ListWords(){
    deleteWords();
}


/**
 * @brief Add word
 * 
 * @param word 
 * @param type 
 */
void ListWords::addWord(std::string word, char type){
    NodeWords *newNode = new NodeWords;
    newNode->word = word;
    newNode->type = type;
    newNode->next = nullptr;

    if(head == nullptr){
        head = newNode;
        tail = newNode;
    }
    else{
        NodeWords *temp = head;
        NodeWords *prev = nullptr;
        while(temp != nullptr){

            // if word == word
            if(temp->word == word){
                
                // if type == type
                if(temp->type == type){
                    delete newNode;
                    break;
                }

                // if type is less, add immediately before
                else if(type < temp->type){
                    if(prev == nullptr){
                        newNode->next = head;
                        head = newNode;
                        break;
                    }else{
                        newNode->next = temp;
                        prev->next = newNode;
                        break;
                    }
                }

                
            }

            else if(word < temp->word){
                if(prev == nullptr){
                    newNode->next = head;
                    head = newNode;
                    break;
                }else{
                    newNode->next = temp;
                    prev->next = newNode;
                    break;
                }
            }
            
            
            if(temp->next == nullptr){
                temp->next = newNode;
                tail = newNode;
                break;
            }

            prev = temp;
            temp = temp->next;
        }
    }
    size++;
}


// add ordered and add meaning if word already exists
void ListWords::addWord(std::string word, char type, std::string meaning){

    NodeWords *newNode = new NodeWords;
    newNode->word = word;
    newNode->type = type;
    newNode->meanings.addMeaning(meaning);
    newNode->next = nullptr;

    if(head == nullptr){
        head = newNode;
        tail = newNode;
    }
    else{
        NodeWords *temp = head;
        NodeWords *prev = nullptr;
        while(temp != nullptr){

            // if word == word
            if(temp->word == word){
                // if type == type, add meaning
                if(temp->type == type){
                    temp->meanings.addMeaning(meaning);
                    delete newNode;
                    break;
                }

                // if type is less, add immediately before
                else if(type < temp->type){
                    if(prev == nullptr){
                        newNode->next = head;
                        head = newNode;
                        break;
                    }else{
                        newNode->next = temp;
                        prev->next = newNode;
                        break;
                    }
                }

                
            }

            else if(word < temp->word){
                if(prev == nullptr){
                    newNode->next = head;
                    head = newNode;
                    break;
                }else{
                    newNode->next = temp;
                    prev->next = newNode;
                    break;
                }
            }
            
            
            if(temp->next == nullptr){
                temp->next = newNode;
                tail = newNode;
                break;
            }

            prev = temp;
            temp = temp->next;
        }
    }
    size++;
}


/**
 * @brief add meaning to a word
 * 
 * @param word 
 * @param type 
 * @param meaning 
 */
void ListWords::addMeaning(std::string word, char type, std::string meaning){
    NodeWords *temp = head;
    while(temp != nullptr){
        if(temp->word == word && temp->type == type){
            temp->meanings.addMeaning(meaning);
            break;
        }
        temp = temp->next;
    }
}



/**
 * @brief search for a word
 * 
 * @param word 
 * @param type 
 * @return NodeWords* 
 */
NodeWords* ListWords::searchWord(std::string word, char type){
    NodeWords *temp = head;
    while(temp != nullptr){
        if(temp->word == word && temp->type == type){
            return temp;
        }
        temp = temp->next;
    }
    return nullptr;
}


/**
 * @brief deletes a word
 * 
 * @param word 
 * @param type 
 */
void ListWords::deleteWord(std::string word, char type){
    NodeWords *temp = head;
    NodeWords *prev = nullptr;
    while(temp != nullptr){
        if(temp->word == word && temp->type == type){
            if(prev == nullptr){
                head = head->next;
                temp->meanings.deleteMeanings();
                delete temp;
                temp = head;
            }else{
                prev->next = temp->next;
                temp->meanings.deleteMeanings();
                delete temp;
                temp = prev->next;
            }
            size--;
            break;
        }
        prev = temp;
        temp = temp->next;
    }
}


/**
 * @brief deletes a word
 * 
 */
void ListWords::deleteWords(){
    NodeWords *temp = head;
    while(temp != nullptr){
        head = head->next;
        temp->meanings.deleteMeanings();
        delete temp;
        temp = head;
    }
    head = nullptr;
    tail = nullptr;
    size = 0;
}

/**
 * @brief deletes words w/ meaning
 * 
 */
void ListWords::deleteWordsWithMeaning(){
    NodeWords *temp = head;
    NodeWords *prev = nullptr;

    while(temp != nullptr){
        prev = temp;
        if(temp->meanings.getSize() >= 1){
            deleteWord(prev->word, prev->type);
        }
        temp = temp->next;
    }
}


// return size of the list
int ListWords::getSize(){
    return size;
}


// prints the list
void ListWords::print(){
    NodeWords *temp = head;
    while(temp != nullptr){
        std::cout << temp->word << " (" << temp->type << ")" <<std::endl;
        temp->meanings.print();
        temp = temp->next;
    }
}


// prints the list to a file
void ListWords::print(std::ostream &out){
    NodeWords *temp = head;
    while(temp != nullptr){
        out << temp->word << " (" << temp->type << ")" <<std::endl;
        temp->meanings.print(out);
        temp = temp->next;
    }
}