#ifndef THREAD_FUNCTIONS_HPP
#define THREAD_FUNCTIONS_HPP

#include <pthread.h>
#include <vector>

#include "sala_class.hpp"
#include "thread_class.hpp"
#include "passa_tempo.hpp"

#include <iostream>

extern std::vector<Sala> salas;

void* thread_function(void* arg);
void entra(int id_sala, int t_id, int last_room);
void sai(int id_sala, int t_id);

#endif