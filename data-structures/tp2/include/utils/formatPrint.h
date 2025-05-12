#include <stdio.h>
#include <string.h>


struct PrintStruct{

    char** Vnames;
    double *Vtimes;
    unsigned *Vn;
    unsigned index {0};
    unsigned size;

    PrintStruct(unsigned size_){
        size = size_;
        unsigned size_arr_print = size * 8; // 7= v1 v2 v3 v4 v5 + merge + heap + special test insertquick
        Vnames = (char**)malloc(size_arr_print *sizeof(char*));
        Vtimes = (double*)malloc(size_arr_print * sizeof(double*));
        Vn = (unsigned*)malloc(size_arr_print * sizeof(unsigned*));
    }

    ~PrintStruct(){
        free(Vnames);
        free(Vtimes);
        free(Vn);
    }

    void addRow(char *name, double time, unsigned n){
        Vnames[index] = name;
        Vtimes[index] = time;
        Vn[index] = n;
        index++;
    }

};


void printHeader(){
    printf("---------------------------------------------------------------------------\n");
    printf("Sort algorithm                Size                  Time                   \n"); 
    printf("---------------------------------------------------------------------------\n");
}


void printTable(char** Vnames, double *Vtimes, unsigned *Vsize, unsigned max_index){
    char number[20];
    char nchar[20];
    for(unsigned i = 0; i<max_index; i++){

        sprintf(number, "%.6f", Vtimes[i]);
        sprintf(nchar, "%u", Vsize[i]);

        printf("%-30s%-22s%-26s\n", Vnames[i], nchar, number);

    }
}

void printFileHeader(char *filename){
    FILE *file = fopen(filename, "w");
    fprintf(file, "---------------------------------------------------------------------------\n");
    fprintf(file, "Sort algorithm                Size                  Time                   \n"); 
    fprintf(file, "---------------------------------------------------------------------------\n");
    fclose(file);
}

void printFileOutput(char** Vnames, double *Vtimes, unsigned *Vsize, unsigned max_index, char* filename){
    FILE *fp;
    fp = fopen(filename, "a");
    char number[20];
    char nchar[20];
    for(unsigned i = 0; i<max_index; i++){

        sprintf(number, "%.6f", Vtimes[i]);
        sprintf(nchar, "%u", Vsize[i]);

        fprintf(fp, "%-30s%-22s%-26s\n", Vnames[i], nchar, number);

    }
    fclose(fp);
}

void printFormatted(PrintStruct &pS){
    printHeader();
    printTable(pS.Vnames, pS.Vtimes, pS.Vn, pS.index);
}


void printFormattedFile(PrintStruct &pS, char* filename){
    printFileHeader(filename);
    printFileOutput(pS.Vnames, pS.Vtimes, pS.Vn, pS.index, filename);
}