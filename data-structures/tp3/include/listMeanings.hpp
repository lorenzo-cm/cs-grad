#ifndef LISTMEANINGS_HPP
#define LISTMEANINGS_HPP

#include <iostream>
#include <fstream>

struct NodeMeanings{
    std::string meaning;
    
    NodeMeanings *next;
};


class ListMeanings{
    private:
        NodeMeanings *head;
        NodeMeanings *tail;
        int size;
    public:
        ListMeanings();
        ~ListMeanings();
        void addMeaning(std::string meaning);
        void deleteMeanings();
        int getSize();

        void print();
        void print(std::ostream &out);
};


#endif