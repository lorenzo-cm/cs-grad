#ifndef AVLTREE_HPP
#define AVLTREE_HPP

#include <iostream>
#include <fstream>
#include "listMeanings.hpp"

struct Node{

    std::string word;
    ListMeanings meanings;
    char type;

    Node *left;
    Node *right;
    int height;

};


class AvlTree{

    private:

        Node *raiz;

        int height(Node *node);
        int max(int a, int b);
        Node* newNode(std::string, char type);
        Node* newNode(std::string, char type, std::string meaning);

        Node* rightRotate(Node*);
        Node* leftRotate(Node*);

        int getBalance(Node*);

        Node* insert(Node *node, std::string word, char type);
        Node* insert(Node *node, std::string word, char type, std::string meaning);

        Node* minValueNode(Node* node);

        Node* deleteNode(Node* root, std::string word, char type);

        void printTree(Node *node);
        void printTree(Node *node, std::ostream &out);

        void deleteTree(Node *node);

        int removeWordsWithMeaning(Node* node);

        // void printInLevelOrder(Node* v);



    public:

        AvlTree();
        ~AvlTree();

        void insert(std::string word, char type);
        void insert(std::string word, char type, std::string meaning);

        void remove(std::string word, char type);

        void print(std::ostream &out);
        void print();

        void deleteTree();

        void removeWordsWithMeaning();





};


#endif