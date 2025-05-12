#include <iostream>
#include "email.h"
#include <string>
#include "memlog.h"

using namespace std;

string trim(string str){
    str.erase(0,str.find_first_not_of(" \n\r\t"));
    str.erase(str.find_last_not_of(" \n\r\t")+1);
    return str;
}

string parseString(string str){
    return trim(str.substr(0, str.find("FIM")));
}


int main(int argc, char** argv){

    if(argc > 1) iniciaMemLog(argv[1]);
    else iniciaMemLog((char*)"out/log.out");
    

    Email email;
    string command;

    while(cin >> command){
        if(command == "CADASTRA"){
            unsigned id;
            cin >> id;

            Messagebox temp(id);

            if(email.push_back(temp) == 1) cout << "OK: CONTA " << id << " CADASTRADA" << endl;
            else cout << "ERRO: CONTA " << id << " JA EXISTENTE" << endl;
        }
        else if(command == "REMOVE"){
            unsigned id;
            cin >> id;

            if(email.remove(id) == 1) cout << "OK: CONTA " << id << " REMOVIDA" << endl;
            else cout << "ERRO: CONTA " << id << " NAO EXISTE" << endl;
        }
        else if(command == "ENTREGA"){
            unsigned id, priority;
            string content;

            cin >> id >> priority;
            getline(cin, content);

            Message msg(content, priority);

            Messagebox* msgbox = email.find(id);

            if(msgbox) {
                msgbox->add_message(msg);
                cout << "OK: MENSAGEM PARA " << id << " ENTREGUE" << endl;
            }
            else cout << "ERRO: CONTA " << id << " NAO EXISTE" << endl;
        }
        else if(command == "CONSULTA"){
            unsigned id; cin >> id;
            Messagebox* msgbox = email.find(id);
            if(msgbox){
                if(!msgbox->isEmpty()) {
                    cout << "CONSULTA " << id << ": " << parseString(msgbox->getHead()) << ' ' << endl;
                    msgbox->pop_back();
                }
                else {
                    cout << "CONSULTA " << id << ": CAIXA DE ENTRADA VAZIA" << endl;
                }
            }
            else cout << "ERRO: CONTA " << id << " NAO EXISTE" << endl;
        }
    }

    finalizaMemLog();

    return 0;
}