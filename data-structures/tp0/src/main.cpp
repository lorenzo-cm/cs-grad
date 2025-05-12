#include "PPMHandler.h"
#include "memlog.h"
#include <getopt.h>
#include "msgassert.h"

using namespace std;

char *input = NULL;
char *output = NULL;

char *plog = NULL;

int mlog = 0;

void help(){
    cerr << "Args: \n"
         << "\t-i <file> input file name*\n"
         << "\t-o <file> output file name* \n"
         << "\t-p <file> activate performance log*\n"
         << "\t-l activate memory log\n"
         << "\t-h help\n"
         << "\t* -- obligatory flags\n";
}


bool checkObligatoryFlags(){
    return input != NULL && output != NULL && plog != NULL;
}

void parse_args(int argc, char** argv){
    int opt;

    while((opt = getopt(argc, argv, "i:o:p:lh")) != EOF)
    {
        switch (opt){

        case 'i':
            input = optarg;
            break;

        case 'o':
            output = optarg;
            break;

        case 'p':
            plog = optarg;
            break;

        case 'l':
            mlog = 1;
            break;

        case 'h':
            default:
                help();
                exit(1);
        }
    }
}

int main(int argc, char** argv){
    
    parse_args(argc,argv);


    erroAssert(checkObligatoryFlags(), "Obligatory flags not running");


    // start memlog
    iniciaMemLog(plog);

    // if memory log == 1, generates the log
    if(mlog) ativaMemLog();
    else desativaMemLog();
    
    Matrix matriz;

    defineFaseMemLog(0);
    if(input) readPPM(matriz, input);

    defineFaseMemLog(1);
    if(output) writePGM(matriz, output);


    // ends memlog
    finalizaMemLog();

    return 0;
}