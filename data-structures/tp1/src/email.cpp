#include "email.h"
#include <iostream>

Email::Email(){
    head = nullptr;
    tail = nullptr;
    size = 0;
}


Email::~Email(){
    Node *temp = head;
    while(temp != nullptr){
        Node *temp2 = temp->next;
        temp = temp->next;
        delete temp2;
    }
}


int Email::push_back(Messagebox _data){
    Node *temp = new Node;
    temp->data = _data;
    temp->next = nullptr;

    // check if empty
    if(head == nullptr){
        head = temp;
        tail = temp;
        size++;
        return 1;
    }

    else {
        
        Node *temp2 = head;
        while(temp2 != nullptr){
            if(temp2->data.getId() == _data.getId()){
                return -1;
            }
            temp2 = temp2->next;
        }

        tail->next = temp;
        tail = temp;
        size++;
        return 1;
    }
}


int Email::remove(unsigned id){
    Node *temp = head;
    Node *prev = head;

    // check if empty
    if(head == nullptr) return -1;

    // check first element
    if(head->data.getId() == id){
        head = head->next;
        delete temp;
        return 1;
    }

    while(temp != nullptr){
        if(temp->data.getId() == id){
            prev->next = temp->next;
            if(tail == temp) tail = prev;
            delete temp;
            size--;
            return 1;
        }
        prev = temp;
        temp = temp->next;
    }

    return -1;
}

Messagebox* Email::find(unsigned id){
    Node *temp = head;
    while(temp != nullptr){
        if(temp->data.getId() == id){
            Messagebox* temp2 = &temp->data;
            return temp2;
        }
        temp = temp->next;
    }
    return nullptr;
}

void Email::print(){
    cout << "--------I-------" << endl;
    Node *temp = head;
    while(temp != nullptr){
        cout << temp->data.getId() << endl;
        temp = temp->next;
    }

    if(tail != nullptr && head != nullptr){
        
        cout << "FIRST" << endl;
        cout << "Head: " << head->data.getId() << endl;
        cout << "Tail: " << tail->data.getId() << endl;
        if(tail->next == nullptr) cout << "Tail next is null" << endl;
        else cout << "Tail next is not null" << endl;
        cout << "- - - - -x- - - -" << endl;
    }

}