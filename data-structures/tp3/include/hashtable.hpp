#ifndef HASHTABLE_HPP
#define HASHTABLE_HPP

#include "listWords.hpp"


class HashTable{
    private:
        ListWords *table;
        int size;
    public:
        HashTable();
        HashTable(int size);
        ~HashTable();
        int hash(std::string word);
        void addWord(std::string word, char type);
        void addWord(std::string word, char type, std::string meaning);
        void addMeaning(std::string word, char type, std::string meaning);
        void deleteWord(std::string word, char type);
        void deleteWordsWithMeaning();
        void deleteHashtable();
        void print();
        void print(std::ostream &out);
};


#endif