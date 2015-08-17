#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char** argv)
{
	if(argc < 3)
	{
		printf("Usage: dir program [args]\n");
		exit(2);
	}
	chdir(argv[1]);
	execv(argv[2], argv+2);
}
