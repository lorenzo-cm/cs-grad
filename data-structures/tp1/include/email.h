#ifndef EMAIL_H
#define EMAIL_H

#include "messagebox.h"
#include "memlog.h"

using namespace std;

class Email{
    private:
        struct Node{
            Messagebox data;
            Node *next;
        };
        Node *head;
        Node *tail;
        int size;

    public:
        Email();
        ~Email();

        int push_back(Messagebox _data);

        int remove(unsigned id);

        Messagebox* find(unsigned id);

        void print();
};




#endif