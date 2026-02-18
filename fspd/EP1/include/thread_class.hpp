#ifndef THREAD_CLASS_HPP
#define THREAD_CLASS_HPP

#include <vector>

class Trajectory {
    public:
        int id_sala;
        int time_min;
        
        Trajectory(int _id_sala, int _time_min);
};


class Thread {
    public:
        int id;
        int t0; // tempo de espera inicial
        int num_salas; // num salas que devem ser visitadas pela thread
        std::vector<Trajectory> trajetoria;

        void add_trajectory(int _id_sala, int _time_min);
};

#endif
