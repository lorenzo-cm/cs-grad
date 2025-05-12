#include "thread_class.hpp"

void Thread::add_trajectory(int _id_sala, int _time_min){
    this->trajetoria.push_back(Trajectory(_id_sala, _time_min));
}

Trajectory::Trajectory(int _id_sala, int _time_min)
    : id_sala(_id_sala), time_min(_time_min) {
}