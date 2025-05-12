#include <cstdio>
#include <string>
#include <iostream>
#include "message.h"

using namespace std;

class Messagebox{
    private:
        struct Node{
            Message data;
            Node *next;
        };
        Node *head;
        Node *tail;
        unsigned id;
        
    public:
        Messagebox();
        Messagebox(unsigned _id);
        ~Messagebox();
        int add_message(Message _message);
        int pop_back();
        unsigned getId();
        string getHead();
        bool isEmpty();

        void print();
};