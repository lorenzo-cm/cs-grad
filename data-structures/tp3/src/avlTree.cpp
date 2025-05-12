#include "avlTree.hpp"
// #include <bits/stdc++.h>

using namespace std;

/**
 * @brief Construct a new Avl Tree:: Avl Tree object
 */
AvlTree::AvlTree(){
	raiz = NULL;
}

/**
 * @brief Destroy the Avl Tree:: Avl Tree object
 */
AvlTree::~AvlTree(){
	deleteTree();
}


/**
 * @brief Return height of the node
 * 
 * @param Node *node
 * @return int height
 */
int AvlTree::height(Node *node)
{
	if (node == NULL)
		return 0;

	return node->height;
}


/**
 * @brief Max function
 * 
 * @param int a
 * @param int b
 * @return int max of a,b
 */
int AvlTree::max(int a, int b)
{
	return (a > b)? a : b;
}


/**
 * @brief Creates a standart new Node with value passed as parameter
 * 
 * @param std::string word 
 * @param char type 
 * @return Node* new node created
 */
Node* AvlTree::newNode(std::string word, char type)
{
	Node* node = new Node();

	node->word = word;
    node->type = type;

	node->left = NULL;
	node->right = NULL;
	node->height = 1; 

	return(node);
}


/**
 * @brief Creates a standart new Node with value passed as parameter
 * 
 * @param std::string word 
 * @param char type 
 * @param std::string meaning 
 * @return Node* new node created
 */
Node* AvlTree::newNode(std::string word, char type, std::string meaning)
{
	Node* node = new Node();

	node->word = word;
    node->type = type;
    node->meanings.addMeaning(meaning);

	node->left = NULL;
	node->right = NULL;
	node->height = 1; 
    
	return(node);
}


/**
 * @brief Right rotation (LL case)
 * 
 * @param Node* y root of the rotation
 * @return Node* new root
 */
Node* AvlTree::rightRotate(Node *y)
{
	Node *x = y->left;
	Node *T2 = x->right;

	x->right = y;
	y->left = T2;

	y->height = max(height(y->left), height(y->right)) + 1;
	x->height = max(height(x->left), height(x->right)) + 1;

	return x;
}

/**
 * @brief Left rotation (RR case)
 * 
 * @param Node* x root of the rotation
 * @return Node* new root
 */
Node* AvlTree::leftRotate(Node *x){
	Node *y = x->right;
	Node *T2 = y->left;

	y->left = x;
	x->right = T2;


	x->height = max(height(x->left), height(x->right)) + 1;
	y->height = max(height(y->left), height(y->right)) + 1;

	return y;
}


/**
 * @brief Calculates a balance of a certain node
 * 
 * @param Node* node
 * @return int the balance factor
 */
int AvlTree::getBalance(Node *N)
{
	if (N == NULL)
		return 0;

	return height(N->left) - height(N->right);
}


/**
 * @brief Insertion of node
 * 
 * @param Node* node to be the root of the insertion
 * @param std::string word 
 * @param char type 
 * @return Node*
 */
Node* AvlTree::insert(Node* node, std::string word, char type)
{
	// Binary search tree rotation and then balances the tree

	if (node == NULL)
		return(newNode(word, type));

	if (word < node->word)
		node->left = insert(node->left, word, type);

	else if (word > node->word)
		node->right = insert(node->right, word, type);

	else if(word == node->word){
        if(type == node->type){
            return node;
        }
        else if(type < node->type){
            node->left = insert(node->left, word, type);
        }
        else{
            node->right = insert(node->right, word, type);
        }
    }

	else return node;

	
	node->height = 1 + max(height(node->left), height(node->right));


	int balance = getBalance(node);


	// Left Left
	if (balance > 1 && word < node->left->word)
		return rightRotate(node);

	// Right Right
	if (balance < -1 && word > node->right->word)
		return leftRotate(node);

	// Left Right Case
	if (balance > 1 && word > node->left->word)
	{
		node->left = leftRotate(node->left);
		return rightRotate(node);
	}

	// Right Left Case
	if (balance < -1 && word < node->right->word)
	{
		node->right = rightRotate(node->right);
		return leftRotate(node);
	}

	
	return node;
}



/**
 * @brief Insertion of node with meaning
 * 
 * @param Node* node to be the root of the insertion
 * @param std::string word 
 * @param char type 
 * @param std::string meaning
 * @return Node*
 */
Node* AvlTree::insert(Node* node, std::string word, char type, std::string meaning){

	// Binary search tree rotation and then balances the tree
	if (node == NULL)
		return(newNode(word, type, meaning));

	if (word < node->word)
		node->left = insert(node->left, word, type, meaning);

	else if (word > node->word)
		node->right = insert(node->right, word, type, meaning);

	else if(word == node->word){
        if(type == node->type){
            node->meanings.addMeaning(meaning);
            return node;
        }
        else if(type < node->type){
            node->left = insert(node->left, word, type, meaning);
        }
        else{
            node->right = insert(node->right, word, type, meaning);
        }
    }
	else return node;

	node->height = 1 + max(height(node->left), height(node->right));

	int balance = getBalance(node);


	// Left Left
	if (balance > 1 && word < node->left->word)
		return rightRotate(node);

	// Right Right
	if (balance < -1 && word > node->right->word)
		return leftRotate(node);

	// Left Right Case
	if (balance > 1 && word > node->left->word){
		node->left = leftRotate(node->left);
		return rightRotate(node);
	}

	// Right Left Case
	if (balance < -1 && word < node->right->word){
		node->right = rightRotate(node->right);
		return leftRotate(node);
	}

	return node;
}


/**
 * @brief Find the sucessor
 * 
 * @param Node* node to be substituted
 * @return Node* 
 */
Node* AvlTree::minValueNode(Node* node){
	Node* current = node;

	while (current->left != NULL)
		current = current->left;

	return current;
}


/**
 * @brief Deletes a node
 * 
 * @param Node* root 
 * @param std::string word 
 * @param char type 
 * @return Node* 
 */
Node* AvlTree::deleteNode(Node* root, std::string word, char type){
	
	if (root == NULL)
		return root;

	if (word < root->word)
		root->left = deleteNode(root->left, word, type);

	else if(word > root->word)
		root->right = deleteNode(root->right, word, type);

	else if( (word == root->word) && (type < root->type) )
		root->left = deleteNode(root->left, word, type);
	
	else if( (word == root->word) && (type > root->type) )
		root->right = deleteNode(root->right, word, type);

	else if( (word == root->word) && (type == root->type) ) {
		// node with only one child or no child
		if( (root->left == NULL) || (root->right == NULL) ){

			
			Node *temp = root->left ? root->left : root->right;

			// No child case
			if (temp == NULL){
				temp = root;
				root = NULL;
			}
			else // One child case
				*root = *temp; 

			free(temp);
		}

		else{
			// node with two children: Get the inorder
			// successor (smallest in the right subtree)
			Node* temp = minValueNode(root->right);

			// Copy the inorder successor's
			// data to this node
			root->word = temp->word;
            root->type = temp->type;
            root->meanings = temp->meanings;

			// Delete the inorder successor
			root->right = deleteNode(root->right, temp->word, temp->type);
		}
	}

	// If the tree had only one node
	// then return
	if (root == NULL)
		return root;

	// STEP 2: UPDATE HEIGHT OF THE CURRENT NODE
	root->height = 1 + max(height(root->left), height(root->right));

	int balance = getBalance(root);


	// Left Left Case
	if (balance > 1 && getBalance(root->left) >= 0)
		return rightRotate(root);

	// Left Right Case
	if (balance > 1 && getBalance(root->left) < 0){
		root->left = leftRotate(root->left);
		return rightRotate(root);
	}

	// Right Right Case
	if (balance < -1 && getBalance(root->right) <= 0)
		return leftRotate(root);

	// Right Left Case
	if (balance < -1 && getBalance(root->right) > 0){
		root->right = rightRotate(root->right);
		return leftRotate(root);
	}

	return root;
}


/**
 * @brief Insert word
 * 
 * @param word 
 * @param type 
 */
void AvlTree::insert(std::string word, char type){
	raiz = insert(raiz, word, type);
};


/**
 * @brief Insert word with meaning
 * 
 * @param word 
 * @param type 
 * @param meaning 
 */
void AvlTree::insert(std::string word, char type, std::string meaning){
	raiz = insert(raiz, word, type, meaning);
};



/**
 * @brief Remove word
 * 
 * @param word 
 * @param type 
 */
void AvlTree::remove(std::string word, char type){
	raiz = deleteNode(raiz, word, type);
}



/**
 * @brief Print in order to a file
 * 
 * @param out 
 */
void AvlTree::print(std::ostream &out){
    printTree(raiz, out);
	// printInLevelOrder(raiz);
}


/**
 * @brief Print auxiliary function (in order)
 * 
 * @param node 
 * @param out 
 */
void AvlTree::printTree(Node *node, std::ostream &out){
    if(node != NULL){
        // in order
        printTree(node->left, out);
        out << node->word << " (" << node->type << ")" << std::endl;
        node->meanings.print(out);
        printTree(node->right, out);
    }
}


/**
 * @brief Print in order
 */
void AvlTree::print(){
    printTree(raiz);
}


/**
 * @brief Auxiliary function to print in order
 * 
 * @param node 
 */
void AvlTree::printTree(Node *node){
    if(node != nullptr){
        // in order
        printTree(node->left);
        std::cout << node->word << " (" << node->type << ")" << std::endl;
        node->meanings.print();
        printTree(node->right);
    }
}



/**
 * @brief Auxiliary delete tree function
 * 
 * @param node 
 */
void AvlTree::deleteTree(Node *node){
    if(node != nullptr){
        node->meanings.deleteMeanings();
        deleteTree(node->left);
        deleteTree(node->right);
        delete node;
    }
}


/**
 * @brief Delete tree function
 */
void AvlTree::deleteTree(){
    deleteTree(raiz);
    raiz = NULL;
}


/**
 * @brief Auxiliary function to remove words w/ meaning
 * 
 * @param node 
 * @return int 
 */
int AvlTree::removeWordsWithMeaning(Node* node){
    if (node != NULL) {
        // se o nodo tiver um significado, remove ele
        if (node->meanings.getSize() > 0) {
            remove(node->word, node->type);
            return 1; // uma vez que volta na raiz, não precisa continuar a função
        }
        return removeWordsWithMeaning(node->left) + removeWordsWithMeaning(node->right);
    } else {
        return 0;
    }
}


/**
 * @brief Function to remove words w/ meaning
 */
void AvlTree::removeWordsWithMeaning() {
    int retorno = removeWordsWithMeaning(this->raiz);
    while (retorno != 0) {
        retorno = removeWordsWithMeaning(this->raiz);
    }
}

// void AvlTree::printInLevelOrder(Node* v){
//     std::queue <Node*> q;
//     Node *cur;

//     q.push(v);
//     q.push(NULL);      

//     while(!q.empty()){
//         cur = q.front();
//         q.pop();
//         if(cur == NULL && q.size()!=0){
//             std::cout<<"\n";
            
//             q.push(NULL);
//             continue;
//         }
//         if(cur!=NULL){
//             std::cout<<" "<<cur->word << " " <<cur->height<<" " << this->getBalance(cur) << " ";

//             if (cur->left!=NULL){
//             q.push(cur->left);
//             }
//             if (cur->right!=NULL){
//                 q.push(cur->right);
//             }
//         }
        
//     }
// }