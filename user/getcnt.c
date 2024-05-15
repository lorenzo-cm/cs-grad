#include "kernel/types.h"
#include "kernel/stat.h"
#include "user/user.h"

#include "kernel/syscall.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(2, "Usage: getcnt syscall_number\n");
        exit(1);
    }

    int num = atoi(argv[1]);
    int count = getcnt(num);

    if (count < 0 || num > NUM_SYSCALLS) {
        fprintf(2, "Invalid syscall number\n");
    } else {
        printf("syscall %d has been called %d times\n", num, count);
    }
    exit(0);
}
