#ifndef DICTIONARY_HASH_HPP
#define DICTIONARY_HASH_HPP

#include "dictionary.hpp"
#include "hashtable.hpp"

class DictionaryHash : public Dictionary{
    private:
        HashTable hashTable;

    public:
        DictionaryHash();
        ~DictionaryHash();
        void insertWord(std::string word, char type, std::string meaning) override;
        void insertWord(std::string word, char type) override;
        void deleteWord(std::string word, char type) override;
        void deleteWordsWithMeaning() override;
        void deleteDictionary() override;
        void print() override;
        void print(std::string filename, char mode) override;

};

#endif