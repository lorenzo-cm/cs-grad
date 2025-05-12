#ifndef DICTIONARY_TREE_HPP
#define DICTIONARY_TREE_HPP

#include "dictionary.hpp"
#include "avlTree.hpp"

class DictionaryTree : public Dictionary{
    private:
        AvlTree tree;
    public:
        DictionaryTree();
        ~DictionaryTree();

        void insertWord(std::string word, char type, std::string meaning) override;
        void insertWord(std::string word, char type) override;
        void deleteWord(std::string word, char type) override;
        void deleteWordsWithMeaning() override;
        void deleteDictionary() override;
        void print() override;
        void print(std::string filename, char mode) override;
};

#endif