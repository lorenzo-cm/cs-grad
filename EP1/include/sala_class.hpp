#ifndef SALA_CLASS_HPP
#define SALA_CLASS_HPP

#include <pthread.h>
#include <queue>

class Sala {

    public:
        pthread_mutex_t mutex;
        pthread_cond_t cond_vazio;
        pthread_cond_t cond_trio;

        int count_esperando;
        int count_dentro;

        std::queue<int> fila_de_espera;
};

#endif