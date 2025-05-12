#include <iostream>
#include <getopt.h>

#include "memlog.h"
#include "sortMem.hpp"
#include "randomize.hpp"

using namespace std;

const int N_MAX_TAM = 100000;

// Global variables for args parsing 

int version = -1;
int s = 0;
int k = 0;
int m = 0;
int n = 0;


// Help menu function
void help(){
    cerr << "Usage: ./sortMem [options]" << endl;
    cerr << "Options:" << endl;
    cerr << "\t -n <int> \t Number of elements to sort" << endl;
    cerr << "\t -s <int> \t Seed for randomization" << endl;
    cerr << "\t -v <int> \t Select algorithm: "<< endl;
    cerr << "\t\t\t 0 - QuickSort" << endl;
    cerr << "\t\t\t 1 - Median of k QuickSort <int>" << endl;
    cerr << "\t\t\t 2 - Selection m QuickSort <int>" << endl;
    cerr << "\t\t\t 3 - Non Recursive QuickSort" << endl;
    cerr << "\t\t\t 4 - Smart Stack QuickSort" << endl;
    cerr << "\t\t\t 5 - MergeSort" << endl;
    cerr << "\t\t\t 6 - HeapSort" << endl;

    cerr << "\t -h \t\t Show this help" << endl;

    // because of a possible memory leak, it's not good to avoid large n
    cerr << "\n\t OBS: Do not test it with a large n" << endl;
}


// Check if the args are valid
bool checkFlags(){
    if(n <= 1){
        cerr << "Error: Number of elements not specified or less than 1" << endl;
        return false;
    }
    if(n>N_MAX_TAM){
        cerr << "Error: Number of elements too large" << endl;
        return false;
    }
    if(version == -1 || version > 6){
        cerr << "Error: Algorithm not specified" << endl;
        return false;
    }
    if(version == 1 && k == 0){
        cerr << "Error: k not specified" << endl;
        return false;
    }
    if(version == 2 && m == 0){
        cerr << "Error: m not specified" << endl;
        return false;
    }
    return true;
}


// Parse the args
void parse_args(int argc, char** argv){
    int opt;

    while((opt = getopt(argc, argv, "v:k:m:n:s:h")) != -1){
        switch(opt){

            case 'v':
                sscanf(optarg, "%d", &version);
                break;

            case 'k':
                sscanf(optarg, "%d", &k);
                break;

            case 'm':
                sscanf(optarg, "%d", &m);
                break;

            case 'n':
                sscanf(optarg, "%d", &n);
                break;

            case 's':
                sscanf(optarg, "%d", &s);
                break;

            case 'h':
                help();
                exit(0);
 
            default:
                cout << "Invalid option. Use -h to see the help message." << endl;
                exit(1);
        }
    }
}


int main(int argc, char** argv){

    parse_args(argc, argv);

    if(!checkFlags()){
        exit(1);
    }

    const int array_size = n;
    const int seed = s;


    // The array has to be static to be able to use the memlog
    Register regArray[array_size];

    // Stores the amount of copies and comparisons
    int *array_cc = nullptr;
    

    //Switch case to select the algorithm
    switch(version){

        case 0:

            // QuickSort

            iniciaMemLog((char*)"out/quicksort.out");
            ativaMemLog();

            defineFaseMemLog(0);

            randomize(regArray, array_size, seed);
            array_cc = quicksort(regArray, 0, array_size-1);

            finalizaMemLog();
            break;

        case 1:

            // Median of k QuickSort

            iniciaMemLog((char*)"out/median_of_k_quicksort.out");
            ativaMemLog();

            randomize(regArray, array_size, seed);
            array_cc = medianQuicksort(regArray, 0, array_size-1, k);

            finalizaMemLog();
            break;

        case 2:

            // Selection m QuickSort

            iniciaMemLog((char*)"out/selection_m_quicksort.out");
            ativaMemLog();

            randomize(regArray, array_size, seed);
            array_cc = selectionQuicksort(regArray, 0, array_size-1, m);

            finalizaMemLog();
            break;
        
        case 3:

            // Non Recursive QuickSort

            iniciaMemLog((char*)"out/non_recursive_quicksort.out");
            ativaMemLog();

            randomize(regArray, array_size, seed);
            array_cc = nrQuicksort(regArray, 0, array_size-1);

            finalizaMemLog();
            break;

        case 4:

            // Smart Stack QuickSort

            iniciaMemLog((char*)"out/smart_stack_quicksort.out");
            ativaMemLog();

            randomize(regArray, array_size, seed);
            array_cc = smartStackQuicksort(regArray, 0, array_size-1);

            finalizaMemLog();
            break;

        case 5:

            // MergeSort

            iniciaMemLog((char*)"out/mergesort.out");
            ativaMemLog();

            randomize(regArray, array_size, seed);
            array_cc = mergesort(regArray, 0, array_size-1);

            finalizaMemLog();
            break;

        case 6:

            // HeapSort

            iniciaMemLog((char*)"out/heapsort.out");
            ativaMemLog();

            randomize(regArray, array_size, seed);
            array_cc = heapsort(regArray, array_size);

            finalizaMemLog();
            break;

    }

    // With mergesort and heapsort is not generated graphics


    // Print the amount of copies and comparisons
    cout    << "Copias = "      << array_cc[0] << endl 
            << "Comparisons = " << array_cc[1] <<  endl;


    delete [] array_cc;

    return 0;
}