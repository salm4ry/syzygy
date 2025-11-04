#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

struct ints {
	short alfa;
	unsigned short bravo;
	int charlie;
	int32_t delta;
	uint64_t echo;
	unsigned int foxtrot;
	long golf;
	unsigned long hotel;
	long long india;
};

struct sizes {
	size_t juliett;
	ssize_t kilo;
};

struct time {
	time_t lima;
};

struct floating_point {
	float mike;
	double november;
	long double oscar;
};

struct pointers {
	char *papa;
	int *quebec;
	double **romeo;
};

struct bytes {
	bool sierra;
	char tango;
	wchar_t uniform;
	unsigned char victor;
};
