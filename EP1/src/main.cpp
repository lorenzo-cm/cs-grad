#include <iostream>
#include "thread_class.hpp"
#include "sala_class.hpp"
#include "thread_functions.hpp"


using namespace std;

vector<Sala> salas;

int main(){

    int S, T;

    cin >> S >> T;

    vector<Thread> threads_data(T);
    salas.resize(S + 1); // 1 ate S

    for (int i = 1; i <= S; ++i) {
        pthread_mutex_init(&salas[i].mutex, nullptr);
        pthread_cond_init(&salas[i].cond_vazio, nullptr);
        pthread_cond_init(&salas[i].cond_trio, nullptr);
        salas[i].count_esperando = 0;
        salas[i].count_dentro = 0;
    }

    for(int i = 0; i<T; i++){
        Thread &data_t = threads_data[i];
        cin >> data_t.id >> data_t.t0 >> data_t.num_salas;

        for(int j = 0; j < data_t.num_salas; j++){
            int id_sala, time_sala;
            cin >> id_sala >> time_sala;
            data_t.add_trajectory(id_sala, time_sala);
        }
    }


    vector<pthread_t> threads(T);

    for (int i = 0; i < T; ++i) {
        Thread* data = &threads_data[i];
        int ret = pthread_create(&threads[i], nullptr, thread_function, (void*)data);
        if (ret != 0) {
            std::cerr << "Error creating thread " << data->id << std::endl;
            exit(EXIT_FAILURE);
        }
    }

    // Join threads
    for (int i = 0; i < T; ++i) {
        pthread_join(threads[i], nullptr);
    }

    // Destroy mutexes and condition variables
    for (int i = 1; i <= S; ++i) {
        pthread_mutex_destroy(&salas[i].mutex);
        pthread_cond_destroy(&salas[i].cond_vazio);
        pthread_cond_destroy(&salas[i].cond_trio);
    }
}