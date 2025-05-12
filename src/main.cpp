#include <iostream>
#include <getopt.h>
#include <stdexcept>
#include <sys/resource.h>

#include "reader.hpp"
#include "randomize.hpp"
#include "memlog.h"
#include "diffTime.hpp"
#include "formatPrint.h"
#include "utils.hpp"

#include "sort.hpp"

const int N_MAX_TAM = 5000000;

// Set global variables for command line options

char *input = NULL;
char *output = NULL;

int version = 0;
int seed = 0;
int k = 0;
int m = 0;

int alwaysQuicksort = 0;

int showProgress = 0;

int notExecuteMergeHeap = 0;


// Print usage information

void help(){
    std::cerr << "Args: \n"
         << "\t-v <int> version of quicksort*\n"
         << "\t\t 1: ordinary quicksort\n"
         << "\t\t 2: median quicksort (k required)\n"
         << "\t\t 3: selection quicksort (m required)\n"
         << "\t\t 4: non recursive quicksort\n"
         << "\t\t 5: smart stack quicksort\n"
         << "\t\t 6: all quicksorts\n"
         << "\t-i <file> input file name* \n"
         << "\t-o <file> output file name* \n"
         << "\t-s <int> seed of the random numbers* \n"

         << "\t-k <int> median of k quicksort\n"
         << "\t-m <int> until which m array size will be used selection sort\n"
         << "\t-q always show recursive quicksort time\n"
         << "\t-p show progress in real time\n"
         << "\t-n not execute mergesort and heapsort\n"
         << "\t-h help\n"
         << "\t* -- obligatory flags\n"
         << "\t<> -- expects a value\n";
}


// Check if the command line arguments are valid
bool checkObligatoryFlags(){

    // not show recursive quicksort 2 times
    if(version == 1 && alwaysQuicksort == 1) version = 0;
    if(version == 6 && alwaysQuicksort == 1) alwaysQuicksort = 0;

    if(version == 2 && k == 0){
        std::cerr << "\nERROR: k is required for median quicksort\n\n";
        return false;
    }

    if(version == 3 && m == 0){
        std::cerr << "\nERROR: m is required for selection quicksort\n\n";
        return false;
    }

    if(version == 6 && (m == 0 || k == 0)){
        std::cerr << "\nERROR: m and k are required version 6\n\n";
        return false;
    }


    return input != NULL && output != NULL && version != 0 && seed != 0;
}


// Parse command line arguments
void parse_args(int argc, char** argv){
    int opt;

    while((opt = getopt(argc, argv, "v:i:o:s:k:m:hqpn")) != EOF)
    {
        switch (opt){

        case 'v':
            sscanf(optarg, "%d", &version);
            if(version < 1 || version > 6) throw std::runtime_error("Invalid version");
            break;

        case 'i':
            input = optarg;
            break;

        case 'o':
            output = optarg;
            break;

        case 's':
            sscanf(optarg, "%d", &seed);
            if(seed < 0) throw std::runtime_error("Negative seed not allowed");
            break;

        case 'k':
            sscanf(optarg, "%d", &k);
            if(k <= 0) throw std::runtime_error("Negative and null k not allowed");
            break;

        case 'm':
            sscanf(optarg, "%d", &m);
            if(m <= 0) throw std::runtime_error("Negative and null m not allowed");
            break;

        case 'q':
            alwaysQuicksort = 1;
            break;

        case 'p':
            showProgress = 1;
            break;

        case 'n':
            notExecuteMergeHeap = 1;
            break;

        case 'h':
            default:
                help();
                exit(1);
        }
    }
}


// Main function
int main(int argc, char** argv){


    // Get the args
    parse_args(argc, argv);


    // Check if the args are valid
    if(!checkObligatoryFlags()) throw std::runtime_error("Obligatory flags missing");


    // Read the input file, store the numbers that represents the size of the array to be sorted and print them
    Reader::readN(input);
    Reader::printN();

    // check if size of array is valid
    for(int i = 0; i < Reader::size; i++){
        if(Reader::valuesN[i] <= 0) throw std::runtime_error("Negative and null n not allowed");
        if(Reader::valuesN[i] >= N_MAX_TAM) throw std::runtime_error("Size of array exceeds the maximum allowed (5,000,000)");
    }

    // Time control
    Register *RegArray;
    struct rusage start, end;
    
    // Print control
    PrintStruct pS(Reader::size);

    // Loop to calculate the time for each array size with certain algorithm
    for(int i = 0; i<Reader::size; i++){

        // if(showProgress) lines will make the program print the progress in real time

        if(showProgress){
            printf("-------------------------------------\n");
            printf("Calculating with n = %d\n", Reader::valuesN[i]);
            printf("-------------------------------------\n");
        }
        
        // Read the input file, store the numbers to be sorted and print them
        RegArray = new Register[Reader::valuesN[i]];
        randomize(RegArray, Reader::valuesN[i], seed);


        // Alway quicksort will make Quicksort always be executed to compare with the other algorithms

        if(alwaysQuicksort){
            getrusage(RUSAGE_SELF, &start);
            quicksort(RegArray, 0, Reader::valuesN[i]-1);
            getrusage(RUSAGE_SELF, &end);

            if(showProgress)
                printf("QUICKSORT RECURSIVE %s\n", isSorted(RegArray, Reader::valuesN[i]) ? "true" : "false");

            pS.addRow((char*)"Recursive Quicksort", diffTime(start, end), Reader::valuesN[i]);
        }

        char aux[10];
        char aux2[50];

        // Execute the algorithm selected by the user (v6 will execute all the algorithms)
        switch (version){

            // Quicksort recursivo
            case 1:

                // Get the time before and after the algorithm execution
                getrusage(RUSAGE_SELF, &start);
                quicksort(RegArray, 0, Reader::valuesN[i]-1);
                getrusage(RUSAGE_SELF, &end);

                if(showProgress)
                    printf("QUICKSORT RECURSIVE %s\n", isSorted(RegArray, Reader::valuesN[i]) ? "true" : "false");


                // Add the row to the print struct with the algorithm name, diff time of before and after the exec and array size
                pS.addRow((char*)"Recursive Quicksort", diffTime(start, end), Reader::valuesN[i]);

                break;


            // Quicksort Mediana k
            case 2:
                
                getrusage(RUSAGE_SELF, &start);
                medianQuicksort(RegArray, 0, Reader::valuesN[i]-1,k);
                getrusage(RUSAGE_SELF, &end);

                if(showProgress)
                    printf("QUICKSORT MEDIAN %s\n", isSorted(RegArray, Reader::valuesN[i]) ? "true" : "false");

                sprintf(aux, "%d", k);
                strcpy(aux2, "Median of "); strcat(aux2, aux); strcat(aux2," Quicksort");
                
                pS.addRow(aux2, diffTime(start, end), Reader::valuesN[i]);

                break;
            

            // Selection Quicksort
            case 3:

                getrusage(RUSAGE_SELF, &start);
                selectionQuicksort(RegArray, 0, Reader::valuesN[i]-1, m);
                getrusage(RUSAGE_SELF, &end);

                if(showProgress)
                    printf("QUICKSORT SELECTION %s\n", isSorted(RegArray, Reader::valuesN[i]) ? "true" : "false");

                sprintf(aux, "%d", m);
                strcpy(aux2, "Selection "); strcat(aux2, aux); strcat(aux2," Quicksort");

                pS.addRow(aux2, diffTime(start, end), Reader::valuesN[i]);

                break;


            // Non-recursive Quicksort
            case 4:
                getrusage(RUSAGE_SELF, &start);
                nrQuicksort(RegArray, 0, Reader::valuesN[i]-1);
                getrusage(RUSAGE_SELF, &end);

                if(showProgress)
                    printf("NON RECURSIVE QUICKSORT RECURSIVE %s\n", isSorted(RegArray, Reader::valuesN[i]) ? "true" : "false");


                pS.addRow((char*)"Non recursive Quicksort", diffTime(start, end), Reader::valuesN[i]);
                break;


            // Smart Stack Quicksort
            case 5:
                getrusage(RUSAGE_SELF, &start);
                smartStackQuicksort(RegArray, 0, Reader::valuesN[i]-1);
                getrusage(RUSAGE_SELF, &end);

                if(showProgress)
                    printf("SMART STACK QUICKSORT RECURSIVE %s\n", isSorted(RegArray, Reader::valuesN[i]) ? "true" : "false");


                pS.addRow((char*)"Smart Stack Quicksort", diffTime(start, end), Reader::valuesN[i]);
                break;
            

            // All
            case 6:

                // Most important for testing, it will execute all the algorithms and print the results

                // Quicksort recursivo
                getrusage(RUSAGE_SELF, &start);
                quicksort(RegArray, 0, Reader::valuesN[i]-1);
                getrusage(RUSAGE_SELF, &end);

                if(showProgress)
                    printf("QUICKSORT RECURSIVE %s\n", isSorted(RegArray, Reader::valuesN[i]) ? "true" : "false");


                pS.addRow((char*)"Recursive Quicksort", diffTime(start, end), Reader::valuesN[i]);


                // Quicksort Mediana k

                randomize(RegArray, Reader::valuesN[i], seed);

                getrusage(RUSAGE_SELF, &start);
                medianQuicksort(RegArray, 0, Reader::valuesN[i]-1,k);
                getrusage(RUSAGE_SELF, &end);

                if(showProgress)
                    printf("QUICKSORT MEDIAN %s\n", isSorted(RegArray, Reader::valuesN[i]) ? "true" : "false");

                sprintf(aux, "%d", k);
                strcpy(aux2, "Median of "); strcat(aux2, aux); strcat(aux2," Quicksort");

                char quicksortmedian[50]; strcpy(quicksortmedian, aux2);
                
                pS.addRow(quicksortmedian, diffTime(start, end), Reader::valuesN[i]);


                // Selection Quicksort

                randomize(RegArray, Reader::valuesN[i], seed);

                getrusage(RUSAGE_SELF, &start);
                selectionQuicksort(RegArray, 0, Reader::valuesN[i]-1, m);
                getrusage(RUSAGE_SELF, &end);

                if(showProgress)
                    printf("QUICKSORT SELECTION %s\n", isSorted(RegArray, Reader::valuesN[i]) ? "true" : "false");

                sprintf(aux, "%d", m);
                strcpy(aux2, "Selection "); strcat(aux2, aux); strcat(aux2," Quicksort");

                char quicksortselection[50]; strcpy(quicksortselection, aux2);
                
                pS.addRow(quicksortselection, diffTime(start, end), Reader::valuesN[i]);


                // Non-recursive Quicksort

                randomize(RegArray, Reader::valuesN[i], seed);

                getrusage(RUSAGE_SELF, &start);
                nrQuicksort(RegArray, 0, Reader::valuesN[i]-1);
                getrusage(RUSAGE_SELF, &end);

                if(showProgress)
                    printf("NON RECURSIVE QUICKSORT RECURSIVE %s\n", isSorted(RegArray, Reader::valuesN[i]) ? "true" : "false");

                pS.addRow((char*)"Non recursive Quicksort", diffTime(start, end), Reader::valuesN[i]);


                // Smart Stack Quicksort

                randomize(RegArray, Reader::valuesN[i], seed);

                getrusage(RUSAGE_SELF, &start);
                smartStackQuicksort(RegArray, 0, Reader::valuesN[i]-1);
                getrusage(RUSAGE_SELF, &end);

                if(showProgress)
                    printf("SMART STACK QUICKSORT RECURSIVE %s\n", isSorted(RegArray, Reader::valuesN[i]) ? "true" : "false");
                
                pS.addRow((char*)"Smart Stack Quicksort", diffTime(start, end), Reader::valuesN[i]);

                break;

            default:
                break;
        }


        // Flag to not execute Merge and Heap sort, cause they are too slow to be tested every time
        if(!notExecuteMergeHeap){
            randomize(RegArray, Reader::valuesN[i], seed);

            getrusage(RUSAGE_SELF, &start);
            mergesort(RegArray, 0, Reader::valuesN[i]-1);
            getrusage(RUSAGE_SELF, &end);

            if(showProgress)
                printf("MERGESORT %s\n", isSorted(RegArray, Reader::valuesN[i]) ? "true" : "false");

            pS.addRow((char*)"Mergesort", diffTime(start, end), Reader::valuesN[i]);



            randomize(RegArray, Reader::valuesN[i], seed);

            getrusage(RUSAGE_SELF, &start);
            heapsort(RegArray, Reader::valuesN[i]);
            getrusage(RUSAGE_SELF, &end);

            if(showProgress)
                printf("HEAPSORT %s\n", isSorted(RegArray, Reader::valuesN[i]) ? "true" : "false");

            pS.addRow((char*)"Heapsort", diffTime(start, end), Reader::valuesN[i]);
        }


        delete[] RegArray;
    }
  
    // Print the results
    printFormatted(pS);

    printFormattedFile(pS, output);


    return 0;
}