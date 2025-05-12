#ifndef SORT_H
#define SORT_H

#include "register.h"
#include "stack.h"

#include <stdlib.h>


void swap(Register *a, Register *b){
    Register aux = *a;
    *a = *b;
    *b = aux;
}


void selectionsortInt(int * array, int n){
    int i, j, min, tmp;
    for(i = 0; i<n-1; i++){
        min = i;
        for(j = i+1; j<n; j++){
            if(array[j] < array[min]) min = j;
        }
        tmp = array[i];
        array[i] = array[min];
        array[min] = tmp;
    }
}


void selectionsortIndex(Register *V, int i, int j){
    for(;i < j; i++){
        int minimum = i;
        for(int k = i + 1; k<=j; k++){
            if(V[k].key < V[minimum].key){
                minimum = k;
            }
        }
        Register aux = V[i];
        V[i] = V[minimum];
        V[minimum] = aux;
    }
}


void insertionsortInt(int * array, int n){
    int i, j, tmp;
    for(i = 1; i<n; i++){
        tmp = array[i];
        j = i-1;
        while(j>=0 && array[j]>tmp){
            array[j+1] = array[j];
            j--;
        }
        array[j+1] = tmp;
    }
}


void insertionsort(Register *V, int n){
    int i, j;
    Register aux;

    for(i = 1; i<n; i++){
        aux = V[i];
        j = i-1;

        while(j>=0 && V[j].key > aux.key){
            V[j+1] = V[j];
            j--;
        }

        V[j+1] = aux;
    }
}


void quicksort( Register * array,  int  left,  int  right) {
     int  i = left, j = right;
     Register tmp;
     int  pivot = array[(left + right) /  2 ].key;
    
     /* partition */
     while  (i <= j) {
         while  (array[i].key < pivot)
            i++;
         while  (array[j].key > pivot)
            j--;
         if  (i <= j) {
            tmp = array[i];
            array[i] = array[j];
            array[j] = tmp;
            i++;
            j--;
        }
    };
    
     /* recursion */
     if  (left < j)
        quicksort(array, left, j);
     if  (i < right)
        quicksort(array, i, right);
}



void selectionQuicksort(Register * array,  int  left,  int  right, int m) {

    if(right-left+1 <= m){
        selectionsortIndex(array, left, right);
        return;
    }

    int  i = left, j = right;

    Register tmp;
    int  pivot = array[(left + right) /  2 ].key;

    /* partition */
    while  (i <= j) {
        while  (array[i].key < pivot)
            i++;
        while  (array[j].key > pivot)
            j--;
        if  (i <= j) {
            tmp = array[i];
            array[i] = array[j];
            array[j] = tmp;
            i++;
            j--;
        }
    };

    /* recursion */
    if  (left < j)
        selectionQuicksort(array, left, j, m);
    if  (i < right)
        selectionQuicksort(array, i, right, m); 
}


int findPivot(Register *V, int i, int j, int k){
    srand(999);

    int arraySize = j-i+1;

    if(k>arraySize) return V[(i + j) /  2 ].key;

    int arrayP[k];

    for(int c = 0; c<k; c++){
        int aux = rand() % arraySize;
        arrayP[c] = V[i + aux].key;
    }

    insertionsortInt(arrayP, k);

    return arrayP[k/2];
}


void medianQuicksort(Register* array, int left, int right, int k){
    int pivot;
    int  i = left, j = right;
    Register tmp;

    pivot = findPivot(array, left, right, k);
    
    /* partition */
    while  (i <= j) {
        while  (array[i].key < pivot)
            i++;
        while  (array[j].key > pivot)
            j--;
        if  (i <= j) {
            tmp = array[i];
            array[i] = array[j];
            array[j] = tmp;
            i++;
            j--;
        }
    };
    
     /* recursion */
     if  (left < j)
        medianQuicksort(array, left, j, k);
     if  (i < right)
        medianQuicksort(array, i, right, k);
}


void nrQuicksort(Register *v, int left, int right){
    Stack stack;
    stack.push(left);
    stack.push(right);
    while(!stack.isEmpty()){
        int r = stack.pop();
        int l = stack.pop();
        int i = l;
        int j = r;
        int pivot = v[(l+r)/2].key;
        while(i <= j){
            while(v[i].key < pivot){
                i++;
            }
            while(v[j].key > pivot){
                j--;
            }
            if(i <= j){
                swap(&v[i], &v[j]);
                i++;
                j--;
            }
        }
        if(l < j){
            stack.push(l);
            stack.push(j);
        }
        if(i < r){
            stack.push(j+1);
            stack.push(r);
        }
    }
}


void smartStackQuicksort(Register *v, int left, int right){
    Stack stack;
    stack.push(left);
    stack.push(right);
    while(!stack.isEmpty()){
        int r = stack.pop();
        int l = stack.pop();
        int i = l;
        int j = r;
        int pivot = v[(l+r)/2].key;
        while(i <= j){
            while(v[i].key < pivot){
                i++;
            }
            while(v[j].key > pivot){
                j--;
            }
            if(i <= j){
                swap(&v[i], &v[j]);
                i++;
                j--;
            }
        }

        int sizeLeft = j - l + 1;
        int sizeRight = r - i + 1;

        if(sizeLeft < sizeRight){
            if(l < j){
                stack.push(l);
                stack.push(j);
            }
            if(i < r){
                stack.push(j+1);
                stack.push(r);
            }
        }else{
            if(i < r){
                stack.push(j+1);
                stack.push(r);
            }
            if(l < j){
                stack.push(l);
                stack.push(j);
            }
        }

    }
}


void merge(Register *V, int init, int mid, int end){


    int nl = mid-init+1;
    int nr = end - mid;

    Register *Vleft = (Register*)malloc(nl * sizeof(Register));
    Register *Vright = (Register*)malloc(nr  * sizeof(Register));

    for(int i = 0; i < nl; i++) Vleft[i] = V[init + i];
    for(int i = 0; i < nr; i++) Vright[i] = V[i + mid+1];
    

    int i = 0;
    int j = 0;
    int k = 0;

    Register *sorted = (Register*)malloc((nl+nr) * sizeof(Register));

    while(i < nl && j < nr){

        if(Vleft[i].key < Vright[j].key){
            sorted[k] = Vleft[i];
            i++;
            
        }else{
            sorted[k] = Vright[j];
            j++;
        }
        k++;
    }

    if(k < nl + nr){

        for(; i<nl; i++){
            sorted[k] = Vleft[i];
            k++;
        }
        for(; j<nr; j++){
            sorted[k] = Vright[j];
            k++;
        }
    }

    for(int h = 0; h< nl + nr; h++){
        V[init + h] = sorted[h];
    }

    free(Vleft);
    free(Vright);
    free(sorted);
}

void mergesort(Register *V, int i, int j){

    if(i<j){
        int mid = (i+j)/2;
        mergesort(V, i, mid);
        mergesort(V, mid+1, j);
        merge(V, i, mid, j);
    }

}


void heapify(Register *V, int n, int i){
    int largest = i;
    int l = 2*i + 1;
    int r = 2*i + 2;

    if(l < n && V[l].key > V[largest].key) largest = l;

    if(r < n && V[r].key > V[largest].key) largest = r;


    if(largest != i){
        Register aux = V[i];
        V[i] = V[largest];
        V[largest] = aux;

        heapify(V, n, largest);
    }
}

void heapsort(Register *V, int n){
    for(int i = n/2 - 1; i>=0; i--){
        heapify(V, n, i);
    }

    for(int i = n-1; i>=0; i--){
        Register aux = V[0];
        V[0] = V[i];
        V[i] = aux;

        heapify(V, i, 0);
    }
}


#endif