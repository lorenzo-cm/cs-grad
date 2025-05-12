#ifndef DICTIONARY_HPP
#define DICTIONARY_HPP


#include <iostream>

class Dictionary{
    private:
        int MAX_SIZE;

    public:
        // Constructor
        Dictionary(){}
        
        // Destructor
        virtual ~Dictionary(){};

        // Inserts words w/ meaning
        virtual void insertWord(std::string word, char type, std::string meaning) = 0;

        // Inserts words
        virtual void insertWord(std::string word, char type) = 0;

        // Deletes words
        virtual void deleteWord(std::string word, char type) = 0;

        // Deletes words with meaning
        virtual void deleteWordsWithMeaning() = 0;

        // Desalocates/deletes the dictionary
        virtual void deleteDictionary() = 0;

        // Prints the dictionary to cout
        virtual void print() = 0;

        // Prints the dictionary to a file
        virtual void print(std::string filename, char mode) = 0;
};

#endif