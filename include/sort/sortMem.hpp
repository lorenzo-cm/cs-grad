// This code has a potencial memory leak, and should not be used in production. It is only for demonstration and analysis purposes.

#ifndef SORT_MEM_H
#define SORT_MEM_H

#include <stdlib.h>

#include "register.h"
#include "stack.h"
#include "memlog.h"

void swap(Register *a, Register *b){
    Register aux = *a;
    *a = *b;
    *b = aux;
    ESCREVEMEMLOG((long)a, sizeof(Register), 0);
    ESCREVEMEMLOG((long)b, sizeof(Register), 0);
}


int* selectionsortInt(int * array, int n){


    int copies = 0;
    int comparisons = 0;

    int i, j, min, tmp;
    for(i = 0; i<n-1; i++){
        min = i;
        for(j = i+1; j<n; j++){
            if(array[j] < array[min]) min = j;
            comparisons++;

            LEMEMLOG((long)&array[j], sizeof(int), 0);
            LEMEMLOG((long)&array[min], sizeof(int), 0);
        }
        tmp = array[i];
        array[i] = array[min];
        array[min] = tmp;
        copies += 3;
    }

    int *array_cc = new int[2]{copies, comparisons};
    return array_cc;
}


int* selectionsortIndex(Register *V, int i, int j){

    int copies = 0;
    int comparisons = 0;

    for(;i < j; i++){
        int minimum = i;
        for(int k = i + 1; k<=j; k++){

            LEMEMLOG((long)&V[k], sizeof(Register), 0);
            LEMEMLOG((long)&V[minimum], sizeof(Register), 0);
            
            if(V[k].key < V[minimum].key){
                minimum = k;
            }
            comparisons++;
        }
        swap(&V[i], &V[minimum]);

        copies += 3;
    }

    int *array_cc = new int[2]{copies, comparisons};
    return array_cc;
}


int* insertionsortInt(int * array, int n){

    int copies = 0;
    int comparisons = 0;

    int i, j, tmp;
    for(i = 1; i<n; i++){
        tmp = array[i];

        LEMEMLOG((long)&array[i], sizeof(int), 0);

        copies++;

        j = i-1;
        while(j>=0 && array[j]>tmp){

            LEMEMLOG((long)&array[j], sizeof(int), 0);

            comparisons += 2;

            array[j+1] = array[j];

            ESCREVEMEMLOG((long)&array[j+1], sizeof(int), 0);

            copies++;

            j--;
        }
        array[j+1] = tmp;

        ESCREVEMEMLOG((long)&array[j+1], sizeof(int), 0);

        copies++;

    }

    int *array_cc = new int[2]{copies, comparisons};
    return array_cc;
}


int* quicksort(Register * array,  int  left,  int  right) {

    int copies = 0;
    int comparisons = 0;

    int  i = left, j = right;
    Register tmp;
    int pivot = array[(left + right) /  2 ].key;
    
    /* partition */
    while  (i <= j) {

        comparisons++;

        while(array[i].key < pivot){
            i++;
            comparisons++;

            LEMEMLOG((long)&array[i], sizeof(Register), 0);
        }

        while(array[j].key > pivot){
            j--;
            comparisons++;

            LEMEMLOG((long)&array[j], sizeof(Register), 0);
        }

        if(i <= j){

            comparisons++;

            swap(&array[i], &array[j]);

            copies += 3;

            i++;
            j--;
        }

    };
    
    int *arrayAux;

    if(left < j){

        comparisons++;

        arrayAux = quicksort(array, left, j);
        copies += arrayAux[0];
        comparisons += arrayAux[1];

        delete[] arrayAux;
    }

    if(i < right){
            
        comparisons++;

        arrayAux = quicksort(array, i, right);
        copies += arrayAux[0];
        comparisons += arrayAux[1];

        delete[] arrayAux;
    }

    int *array_cc = new int[2]{copies, comparisons};
    return array_cc;
}



int* selectionQuicksort(Register * array,  int  left,  int  right, int m) {

    if(right-left+1 <= m){
        int *arrayAux = selectionsortIndex(array, left, right);
        return arrayAux;
    }

    int copies = 0;
    int comparisons = 1;

    int  i = left, j = right;

    Register tmp;
    int  pivot = array[(left + right) /  2 ].key;

    /* partition */
    while(i <= j){

        comparisons++;

        while(array[i].key < pivot){
            i++;
            comparisons++;

            LEMEMLOG((long)&array[i], sizeof(Register), 0);
        }

        while(array[j].key > pivot){
            j--;
            comparisons++;

            LEMEMLOG((long)&array[j], sizeof(Register), 0);
        }

        if(i <= j){

            comparisons++;

            swap(&array[i], &array[j]);

            copies += 3;

            i++;
            j--;
        }
    };

    int *arrayAux;

    if(left < j){
        comparisons++;
        
        arrayAux = selectionQuicksort(array, left, j, m);
        copies += arrayAux[0];
        comparisons += arrayAux[1];

        delete[] arrayAux;
    }
        

    if(i < right){
        comparisons++;

        arrayAux = selectionQuicksort(array, i, right, m);
        copies += arrayAux[0];
        comparisons += arrayAux[1];

        delete[] arrayAux;
    }

    int *array_cc = new int[2]{copies, comparisons};
    return array_cc; 
}


int findPivot(Register *V, int i, int j, int k, int copies, int comparisons){
    srand(999);

    int arraySize = j-i+1;

    if(k>arraySize) return V[(i + j) /  2 ].key;

    comparisons++;

    int arrayP[k];

    for(int c = 0; c<k; c++){
        int aux = rand() % arraySize;
        arrayP[c] = V[i + aux].key;

        LEMEMLOG((long)&V[i + aux], sizeof(Register), 0);
    }

    int *arrayAux = insertionsortInt(arrayP, k);

    copies += arrayAux[0];
    comparisons += arrayAux[1];

    delete[] arrayAux;

    return arrayP[k/2];
}


int* medianQuicksort(Register* array, int left, int right, int k){

    int copies = 0;
    int comparisons = 0;

    int pivot;
    int  i = left, j = right;
    Register tmp;

    pivot = findPivot(array, left, right, k, copies, comparisons);

    comparisons++;
    
    /* partition */
    while(i <= j) {

        comparisons++;

        while(array[i].key < pivot){
            i++;
            comparisons++;

            LEMEMLOG((long)&array[i], sizeof(Register), 0);
        }

        while(array[j].key > pivot){
            j--;
            comparisons++;

            LEMEMLOG((long)&array[j], sizeof(Register), 0);
        }

        if(i <= j){
            
            comparisons++;

            swap(&array[i], &array[j]);

            copies += 3;

            i++;
            j--;
        }
    }
    
    int *arrayAux;

    if(left < j){

        comparisons++;

        arrayAux = medianQuicksort(array, left, j, k);
        copies += arrayAux[0];
        comparisons += arrayAux[1];

        delete[] arrayAux;
    }
        

    if(i < right){
        
        comparisons++;

        arrayAux = medianQuicksort(array, i, right, k);
        copies += arrayAux[0];
        comparisons += arrayAux[1];

        delete[] arrayAux;
    }

    int *array_cc = new int[2]{copies, comparisons};
    return array_cc;
}


int* nrQuicksort(Register *v, int left, int right){

    int copies = 0;
    int comparisons = 0;

    Stack stack;
    stack.push(left);
    stack.push(right);

    while(!stack.isEmpty()){

        comparisons++;

        int r = stack.pop();
        int l = stack.pop();
        int i = l;
        int j = r;
        int pivot = v[(l+r)/2].key;

        while(i <= j){
            
            comparisons++;

            while(v[i].key < pivot){
                i++;
                comparisons++;

                LEMEMLOG((long)&v[i], sizeof(Register), 0);
            }

            while(v[j].key > pivot){
                j--;
                comparisons++;

                LEMEMLOG((long)&v[j], sizeof(Register), 0);
            }

            if(i <= j){

                comparisons++;

                swap(&v[i], &v[j]);
                copies += 3;
                i++;
                j--;
            }
        }

        if(l < j){

            comparisons++;

            stack.push(l);
            stack.push(j);
        }

        if(i < r){

            comparisons++;

            stack.push(j+1);
            stack.push(r);
        }
    }

    int *array_cc = new int[2]{copies, comparisons};
    return array_cc;
}


int* smartStackQuicksort(Register *v, int left, int right){

    int copies = 0;
    int comparisons = 0;

    Stack stack;
    stack.push(left);
    stack.push(right);

    while(!stack.isEmpty()){

        comparisons++;

        int r = stack.pop();
        int l = stack.pop();
        int i = l;
        int j = r;
        int pivot = v[(l+r)/2].key;
        while(i <= j){

            comparisons++;

            while(v[i].key < pivot){
                i++;
                comparisons++;

                LEMEMLOG((long)&v[i], sizeof(Register), 0);
            }

            while(v[j].key > pivot){
                j--;
                comparisons++;

                LEMEMLOG((long)&v[j], sizeof(Register), 0);
            }

            if(i <= j){

                comparisons++;

                swap(&v[i], &v[j]);
                copies += 3;
                i++;
                j--;
            }
        }

        int sizeLeft = j - l + 1;
        int sizeRight = r - i + 1;

        if(sizeLeft < sizeRight){

            comparisons++;

            if(l < j){

                comparisons++;

                stack.push(l);
                stack.push(j);
            }
            if(i < r){

                comparisons++;

                stack.push(j+1);
                stack.push(r);
            }
        }else{

            comparisons++;

            if(i < r){

                comparisons++;

                stack.push(j+1);
                stack.push(r);
            }
            if(l < j){

                comparisons++;

                stack.push(l);
                stack.push(j);
            }
        }

    }

    int *array_cc = new int[2]{copies, comparisons};
    return array_cc;
}


int* merge(Register *V, int init, int mid, int end){

    int copies = 0;
    int comparisons = 0;

    int nl = mid-init+1;
    int nr = end - mid;

    Register *Vleft = (Register*)malloc(nl * sizeof(Register));
    Register *Vright = (Register*)malloc(nr  * sizeof(Register));

    for(int i = 0; i < nl; i++){
        Vleft[i] = V[init + i];
        copies++;
    }
    
    for(int i = 0; i < nr; i++){
        Vright[i] = V[i + mid+1];
        copies++;
    }
    

    int i = 0;
    int j = 0;
    int k = 0;

    Register *sorted = (Register*)malloc((nl+nr) * sizeof(Register));

    while(i < nl && j < nr){

        comparisons += 2;

        if(Vleft[i].key < Vright[j].key){
            sorted[k] = Vleft[i];

            comparisons++;
            copies++;

            i++;
            
        }else{
            sorted[k] = Vright[j];

            comparisons++;
            copies++;

            j++;
        }
        k++;
    }

    if(k < nl + nr){

        comparisons++;

        for(; i<nl; i++){
            sorted[k] = Vleft[i];

            copies++;

            k++;
        }
        for(; j<nr; j++){
            sorted[k] = Vright[j];

            copies++;

            k++;
        }
    }

    for(int h = 0; h< nl + nr; h++){
        V[init + h] = sorted[h];

        copies++;

    }

    free(Vleft);
    free(Vright);
    free(sorted);

    int *array_cc = new int[2]{copies, comparisons};
    return array_cc;
}

int* mergesort(Register *V, int i, int j){

    int copies = 0;
    int comparisons = 0;

    if(i<j){

        comparisons++;

        int mid = (i+j)/2;

        int *arrayAux;

        arrayAux = mergesort(V, i, mid);

        copies += arrayAux[0];
        comparisons += arrayAux[1];

        delete[] arrayAux;

        arrayAux = mergesort(V, mid+1, j);

        copies += arrayAux[0];
        comparisons += arrayAux[1];

        delete[] arrayAux;

        arrayAux = merge(V, i, mid, j);

        copies += arrayAux[0];
        comparisons += arrayAux[1];

        delete[] arrayAux;
    }

    comparisons++;

    int *array_cc = new int[2]{copies, comparisons};
    return array_cc;

}


int* heapify(Register *V, int n, int i){

    int copies = 0;
    int comparisons = 0;

    int *arrayAux;

    int largest = i;
    int l = 2*i + 1;
    int r = 2*i + 2;

    if(l < n && V[l].key > V[largest].key){
        largest = l;
    }

    comparisons += 2;

    if(r < n && V[r].key > V[largest].key){
        largest = r;
    }

    comparisons += 2;


    if(largest != i){

        comparisons++;

        Register aux = V[i];
        V[i] = V[largest];
        V[largest] = aux;

        copies += 3;

        arrayAux = heapify(V, n, largest);

        copies += arrayAux[0];
        comparisons += arrayAux[1];

        delete[] arrayAux;
    }

    int *array_cc = new int[2]{copies, comparisons};
    return array_cc;
}

int* heapsort(Register *V, int n){

    int copies = 0;
    int comparisons = 0;

    int* arrayAux;

    for(int i = n/2 - 1; i>=0; i--){
        arrayAux = heapify(V, n, i);

        copies += arrayAux[0];
        comparisons += arrayAux[1];

        delete[] arrayAux;
    }

    for(int i = n-1; i>=0; i--){
        Register aux = V[0];
        V[0] = V[i];
        V[i] = aux;

        copies += 3;

        arrayAux = heapify(V, i, 0);

        copies += arrayAux[0];
        comparisons += arrayAux[1];

        delete[] arrayAux;
    }

    int *array_cc = new int[2]{copies, comparisons};
    return array_cc;
}


#endif