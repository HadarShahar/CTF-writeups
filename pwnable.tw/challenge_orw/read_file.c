#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main(int argc, char *argv[]) {
    int fd = open("exp.py", O_RDONLY);
    char buffer[1024];
    int n = read(fd, buffer, sizeof(buffer));
    write(1, buffer, n);
}
