#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

int main(int argc, char *argv[]) {
    // 1 additional argument = number 
    if (argc != 2) {
        fprintf(2, "Usage: settickets num_tickets\n");
        exit(1);
    }

    int num_tickets = atoi(argv[1]);
    if (num_tickets < 1) {
        fprintf(2, "Error: num_tickets must be at least 1\n");
        exit(1);
    }

    int result = settickets(num_tickets);
    if (result < 0) {
        fprintf(2, "Error setting tickets\n");
        exit(1);
    }

    exit(0);
}
