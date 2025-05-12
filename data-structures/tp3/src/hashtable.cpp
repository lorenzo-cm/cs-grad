#include "hashtable.hpp"


/**
 * @brief Construct a new Hash Table:: Hash Table object
 */
HashTable::HashTable(){
    size = 78 * 78; // ascii - to z first letter and second letter
    table = new ListWords[size];
}


/**
 * @brief Construct a new Hash Table:: Hash Table object
 * 
 * @param size 
 */
HashTable::HashTable(int size){
    this->size = size;
    table = new ListWords[size];
}


/**
 * @brief Destroy the Hash Table:: Hash Table object
 */
HashTable::~HashTable(){
    deleteHashtable();
    delete[] table;
}


/**
 * @brief Codes the word and returns the index
 * 
 * @param word 
 * @return int index
 */
int HashTable::hash(std::string word){
    int index = 0;

    if(word.length() == 1) index = (word[0] - '-') * 78;

    else index = (word[0] - '-')*78 + (word[1] - '-');

    return index;
}


/**
 * @brief Add word into hashtable
 * 
 * @param word 
 * @param type 
 */
void HashTable::addWord(std::string word, char type){
    int index = hash(word);
    table[index].addWord(word, type);
}


/**
 * @brief Add word with meaning into hashtable
 * 
 * @param word 
 * @param type 
 * @param meaning 
 */
void HashTable::addWord(std::string word, char type, std::string meaning){
    int index = hash(word);
    table[index].addWord(word, type, meaning);
}


/**
 * @brief Add meaning to a alredy existing word
 * 
 * @param word 
 * @param type 
 * @param meaning 
 */
void HashTable::addMeaning(std::string word, char type, std::string meaning){
    int index = hash(word);
    table[index].addMeaning(word, type, meaning);
}


/**
 * @brief Deletes a word
 * 
 * @param word 
 * @param type 
 */
void HashTable::deleteWord(std::string word, char type){
    int index = hash(word);
    table[index].deleteWord(word, type);
}


/**
 * @brief Deletes word with meaning
 */
void HashTable::deleteWordsWithMeaning(){
    for(int i = 0; i < size; i++){
        table[i].deleteWordsWithMeaning();
    }
}


/**
 * @brief Deletes/desalocate Hashtable
 */
void HashTable::deleteHashtable(){
    for(int i = 0; i < size; i++){
        table[i].deleteWords();
    }
}


// Print hashtable
void HashTable::print(){

    // print the words that start with capital letters first
    table[26*26].print();

    for(int i = 0; i < size-1; i++){
        table[i].print();
    }
}

// Print hashtable into a file
void HashTable::print(std::ostream &out){

    // print the words that start with capital letters first
    table[26*26].print(out);

    for(int i = 0; i < size-1; i++){
        table[i].print(out);
    }
}