#include "messagebox.h"

using namespace std;

Messagebox::Messagebox(){
    head = nullptr;
    tail = nullptr;
    id = 0;
}

Messagebox::Messagebox(unsigned _id){
    head = nullptr;
    tail = nullptr;
    id = _id;
}

Messagebox::~Messagebox(){
    while(head != nullptr){
        pop_back();
    }
}

// Add in decreasing order of priority
int Messagebox::add_message(Message _message){
    Node *temp = new Node;
    temp->data = _message;
    temp->next = nullptr;

    // check if empty
    if(head == nullptr){
        head = temp;
        tail = temp;
        return 1;
    }
    else {
        Node *temp2 = head;
        Node *prev = head;
        while(temp2 != nullptr){
            if(_message.priority > temp2->data.priority){
                // check if 1 element
                if(temp2 == head){
                    temp->next = head;
                    head = temp;
                    return 2;
                }
                else {
                    temp->next = temp2;
                    prev->next = temp;
                    return 3;
                }
            }
            else{
                if(temp2->next == nullptr){
                    temp2->next = temp;
                    return 4;
                }
            }
            prev = temp2;
            temp2 = temp2->next;
        }
        return -1;
    }
}

int Messagebox::pop_back(){
    Node *temp = head;

    // check if empty
    if(head == nullptr) return -1;

    // check if 1 element
    if(head->next == nullptr){
        head = nullptr;
        delete temp;
        return 1;
    }

    head = head->next;
    delete temp;
    return 1;
}

unsigned Messagebox::getId(){
    return id;
}

string Messagebox::getHead(){
    return head->data.content;
}

bool Messagebox::isEmpty(){
    if(head == nullptr) return true;
    else return false;
}

void Messagebox::print(){
    Node *temp = head;
    while(temp != nullptr){
        cout << temp->data.content << " ";
        temp = temp->next;
    }
    cout << endl;
}