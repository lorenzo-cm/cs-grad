#include "dictionaryHash.hpp"


DictionaryHash::DictionaryHash(){}


DictionaryHash::~DictionaryHash(){
    deleteDictionary();
}


void DictionaryHash::insertWord(std::string word, char type, std::string meaning){
    hashTable.addWord(word, type, meaning);
}


void DictionaryHash::insertWord(std::string word, char type){
    hashTable.addWord(word, type);
}


void DictionaryHash::deleteWord(std::string word, char type){
    hashTable.deleteWord(word, type);
}


void DictionaryHash::deleteWordsWithMeaning(){
    hashTable.deleteWordsWithMeaning();
}


void DictionaryHash::deleteDictionary(){
    hashTable.deleteHashtable();
}


void DictionaryHash::print(){
    hashTable.print();
}


void DictionaryHash::print(std::string filename, char mode){
    if(mode == 'a'){
        std::ofstream file(filename, std::fstream::app);
        hashTable.print(file);
        file.close();
    }
    else{
        std::ofstream file(filename);
        hashTable.print(file);
        file.close();    
    }
}