#include "thread_functions.hpp"

bool verbose = false;

void* thread_function(void* arg){
    Thread* data = (Thread*)arg;
    int t_id = data->id;

    passa_tempo(t_id, 0, data->t0);

    if(verbose) std::cout<<"fim espera inicial "<< t_id << "\n";

    int last_room = -1; 
    for (size_t i = 0; i < data->trajetoria.size(); ++i) {
        int current_room = data->trajetoria[i].id_sala;
        int time_in_room = data->trajetoria[i].time_min;

        entra(current_room, t_id, last_room);
        last_room = current_room;

        passa_tempo(t_id, current_room, time_in_room);
    }

    sai(last_room, t_id);

    pthread_exit(nullptr);
}

void entra(int id_sala, int t_id, int last_room){
    pthread_mutex_lock(&salas[id_sala].mutex);

    while(salas[id_sala].count_dentro > 0){
        if(verbose) std::cout << t_id << "esperando! A sala " << id_sala << " esta cheia \n";
        pthread_cond_wait(&salas[id_sala].cond_vazio, &salas[id_sala].mutex);
    }

    salas[id_sala].count_esperando++;

    if(salas[id_sala].count_esperando < 3){
        while(salas[id_sala].count_esperando < 3) {
            if(verbose) std::cout << t_id << " esperando! Faltam " << 3 - salas[id_sala].count_esperando  << " threads na sala " << id_sala <<" \n";
            pthread_cond_wait(&salas[id_sala].cond_trio, &salas[id_sala].mutex);
        }
    }

    else{
        if(verbose) std::cout << "entrou aqui" << "\n";
        salas[id_sala].count_dentro = 3;
        pthread_cond_broadcast(&salas[id_sala].cond_trio);
    }

    if (last_room != -1){
        sai(last_room, t_id);
    }

    if(verbose) std::cout << "entrou " << t_id <<" na sala " << id_sala << " \n";

    pthread_mutex_unlock(&salas[id_sala].mutex);
}

void sai(int id_sala, int t_id){
    pthread_mutex_lock(&salas[id_sala].mutex);

    salas[id_sala].count_dentro--;

    if(verbose) std::cout << t_id << " saindo da sala " << id_sala << "\n";

    if(salas[id_sala].count_dentro == 0){
        salas[id_sala].count_esperando = 0;
        pthread_cond_broadcast(&salas[id_sala].cond_vazio);
    }

    pthread_mutex_unlock(&salas[id_sala].mutex);
}