#ifndef LISTWORDS_HPP
#define LISTWORDS_HPP

#include "listMeanings.hpp"

struct NodeWords
{
    std::string word;
    char type;
    ListMeanings meanings;

    NodeWords *next;
};


class ListWords
{
    private:
        NodeWords *head;
        NodeWords *tail;
        int size;
    public:
        ListWords();
        ~ListWords();
        void addWord(std::string word, char type);
        void addWord(std::string word, char type, std::string meaning);
        void addMeaning(std::string word, char type, std::string meaning);
        NodeWords* searchWord(std::string word, char type);
        void deleteWord(std::string word, char type);
        void deleteWords();
        void deleteWordsWithMeaning();
        int getSize();

        void print();
        void print(std::ostream &out);

};



#endif