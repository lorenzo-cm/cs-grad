#include <fstream>
#include <iostream>

using namespace std;

int main(int argc, char** argv){
    ofstream file;
    file.open(argv[1]);
    for(int i = 0; i<10000; i++){
        file << "CADASTRA " << i << endl;
        for(int j = 0; j<1; j++){
            file << "ENTREGA " << i << " 1 MENSAGEM2" << " FIM" << endl;
        }
        for(int j = 0; j<1; j++){
            file << "CONSULTA " << i << endl;
        }
        file << "REMOVE " << i << endl;
    }
}