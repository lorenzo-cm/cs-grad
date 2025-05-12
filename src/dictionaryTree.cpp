#include "dictionaryTree.hpp"

DictionaryTree::DictionaryTree(){}


DictionaryTree::~DictionaryTree(){
    deleteDictionary();
}


void DictionaryTree::insertWord(std::string word, char type, std::string meaning){
    tree.insert(word, type, meaning);
}


void DictionaryTree::insertWord(std::string word, char type){
    tree.insert(word, type);
}


void DictionaryTree::deleteWord(std::string word, char type){
    tree.remove(word, type);
}


void DictionaryTree::deleteWordsWithMeaning(){
    tree.removeWordsWithMeaning();
}


void DictionaryTree::deleteDictionary(){
    tree.deleteTree();
}


void DictionaryTree::print(){
    tree.print();
}


void DictionaryTree::print(std::string filename, char mode){
    if(mode == 'a'){
        std::ofstream file(filename, std::fstream::app);
        tree.print(file);
        file.close();
    }
    else{
        std::ofstream file(filename);
        tree.print(file);
        file.close();    
    }
}