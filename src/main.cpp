#include <getopt.h>
#include <iostream>

#include "dictionaryHash.hpp"
#include "dictionaryTree.hpp"
#include "msgassert.h"
#include "memlog.h"
#include "reader.hpp"

using namespace std;

// Global variables
char* input;
char* output;
string data_structure;

// Print the help
void help(){
    cout << "Usage: ./main -i <input file> -o <output file> -t <data structure>" << endl;
    cout << "data structure: \"hash\" or \"tree\"" << endl;
    cout << "Example: ./main -i ent.txt -o out.txt -t hash" << endl;
}

// Check if the args are valid
bool checkArgs(){
    if(input == NULL || output == NULL || data_structure == "NULL") return false;
    return true;
}

// Get the args and put them in the global variables
void parse_args(int argc, char** argv){
    int opt;

    while((opt = getopt(argc, argv, "i:o:t:")) != EOF)
    {
        switch (opt){

        case 'i':
            input = optarg;
            break;

        case 'o':
            output = optarg;
            break;

        case 't':
            data_structure = optarg;
            break;

        case 'h':
            default:
                help();
                exit(1);
        }
    }
}

int main(int argc, char** argv){

    data_structure = "NULL";

    // Get the args
    parse_args(argc, argv);

    // Check if the args are valid
    if(!checkArgs()) erroAssert(0, "Invalid or Missing arguments");

    Dictionary *dict;

    // Print the data structure
    if(data_structure == "hash") std::cout << "hash" << std::endl;
    else if(data_structure == "tree") std::cout << "tree" << std::endl;
    else std::cout << "invalid" << std::endl;

    // Create the dictionary based on the data structure

    if(data_structure == "hash"){
        dict = new DictionaryHash;
    }
    else if(data_structure == "tree"){
        dict = new DictionaryTree;
    }
    else erroAssert(0, "Invalid data structure");

    string output_ = "out/output_";
    string end_ = ".txt";
    output_ += data_structure;
    output_ += end_;

    // Start the memory log
    iniciaMemLog((char*)output_.c_str());

    // start the actual program

    // Read the file
    reader(input, *dict);

    dict->print(output, 'w');

    cout << "Deleting" << endl;

    dict->deleteWordsWithMeaning();

    dict->print(output, 'a');

    // End the memory log
    finalizaMemLog();

    // Delete the dictionary
    delete dict;
    
    return 0;
}