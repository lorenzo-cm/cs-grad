#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

#include "kernel/pstat.h"

int main(int argc, char *argv[]) {
    struct pstat pst;

    // Invoke the getpinfo system call
    if (getpinfo(&pst) < 0) {
        printf("Error: getpinfo system call failed\n");
        exit(1);
    }

    // Print process information
    printf("PID\tTickets\tTicks\n");
    for (int i = 0; i < NPROC; i++) {
        if (pst.inuse[i]) {
            printf("%d\t%d\t%d\n", pst.pid[i], pst.tickets[i], pst.ticks[i]);
        }
    }

    return 0;
}
