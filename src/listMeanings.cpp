#include "listMeanings.hpp"


/**
 * @brief Construct a new List Meanings:: List Meanings object -> head = tail = NULL , size 0
 */
ListMeanings::ListMeanings(){
    head = NULL;
    tail = NULL;
    size = 0;
}


/**
 * @brief Destroy the List Meanings:: List Meanings object
 */
ListMeanings::~ListMeanings(){
    deleteMeanings();
}


/**
 * @brief Add meaning to a word
 * 
 * @param meaning 
 */
void ListMeanings::addMeaning(std::string meaning){
    NodeMeanings *newNode = new NodeMeanings;
    newNode->meaning = meaning;
    newNode->next = NULL;
    
    if(head == NULL){
        head = newNode;
        tail = newNode;
    }else{
        tail->next = newNode;
        tail = newNode;
    }
    size++;
}


/**
 * @brief Delete all meanings of one word
 */
void ListMeanings::deleteMeanings(){
    NodeMeanings *temp = head;
    while(temp != NULL){
        head = head->next;
        delete temp;
        temp = head;
    }
    head = NULL;
    tail = NULL;
    size = 0;
}


/**
 * @brief Get how many meanings a word has
 * 
 * @return int 
 */
int ListMeanings::getSize(){
    return size;
}


/**
 * @brief prints the meanings
 */
void ListMeanings::print(){
    NodeMeanings *temp = head;
    int i = 1;
    while(temp != NULL){
        std::cout << i << ". " << temp->meaning << std::endl;
        i++;
        temp = temp->next;
    }
}


/**
 * @brief prints the meanings into a file
 * 
 * @param out 
 */
void ListMeanings::print(std::ostream &out){
    NodeMeanings *temp = head;
    int i = 1;
    while(temp != NULL){
        out << i << ". " << temp->meaning << std::endl;
        i++;
        temp = temp->next;
    }
}