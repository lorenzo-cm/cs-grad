#ifndef EXCEPTION_H
#define EXCEPTION_H
#include<iostream>

using namespace std;

class Exception{
    protected:
        string texto = "Exception";
    public:
        virtual void what(){
            cerr << this->texto << endl;
        };
};

class matchException : public Exception{
    public:
        matchException() {texto = "Não foi possível fazer o match";}
};

class invalidPassword : public Exception{
    public:
        invalidPassword(){texto = "Senha inválida";}
};

class userNotFound : public Exception{
    public:
        userNotFound(){texto = "Usuário inválido";}
};

class usernameAlreadyInUse : public Exception{
    public:
        usernameAlreadyInUse(){texto = "Nome de usuário já está em uso";}
};

class invalidNumber : public Exception {
    public:
        invalidNumber(){texto = "Número inválido";}
};


class invalidAge : public Exception {
    public:
        invalidAge(){texto = "Idade inválida";}
};

class invalidGender : public Exception {
    public:
        invalidGender(){texto = "Sexo inválido";}
};

class sendMessageError : public Exception{
    public:
        sendMessageError(){texto = "Não foi possível enviar a mensagem";}
};

class NotFriend : public Exception{
    public:
        NotFriend(){texto = "O usuário em questão não é seu amigo :(";}
};

class createUserError : public Exception{
    public:
        createUserError(){texto = "Não foi possível criar conta";}
};

#endif