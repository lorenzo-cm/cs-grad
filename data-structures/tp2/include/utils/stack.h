#ifndef STACK_H
#define STACK_H

#include "register.h"

const int MAX_TAM = 1000000;


struct Node{
    Node *next;
    int index;

    Node(int i) : index{i} {}
};


struct Stack{

    Node *top;
    int size;

    Stack() : top{nullptr}, size{0} {}

    void push(int index){
        Node *newNode = new Node(index);
        newNode->next = top;
        top = newNode;
        size++;
    }

    int pop(){
        if(top == nullptr){
            return -1;
        }
        int index = top->index;
        Node *aux = top;
        top = top->next;
        delete aux;
        size--;
        return index;
    }

    bool isEmpty(){
        return top == nullptr;
    }


    int getSize(){
        return size;
    }

    void clear(){
        while(!isEmpty()){
            pop();
        }
    }

 
};
    

#endif