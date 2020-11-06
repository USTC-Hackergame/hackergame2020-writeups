#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

extern int evil();

char buffer[16536];
int main() {
	evil();
	int fd = open("/proc/self/maps", 0);
	int size = read(fd, buffer, sizeof(buffer));
	if (size > 0)
		write(0, buffer, size);
	return 0;
}
