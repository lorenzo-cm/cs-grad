#include <fstream>
#include <iostream>
#include <stdio.h>

#include "msgassert.h"
#include "dictionary.hpp"


/**
 * @brief Reads the input in .txt file and inserts into the dictionary passed as parameter
 * 
 * @param fileName 
 * @param dictionary 
 */
void reader(std::string fileName, Dictionary &dictionary){

    std::ifstream file(fileName);


    erroAssert(file.is_open(), "Erro ao abrir o arquivo");

    std::string word, meaning;
    char type;

    meaning = "";

    while(file >> type){
        getline(file, word, ']');
        getline(file, meaning);

        word.erase(0, 2);

        meaning.erase(0, 1);
        
        if(meaning == "") dictionary.insertWord(word, type);
        else dictionary.insertWord(word, type, meaning);

        meaning = "";
    }

    file.close();
}