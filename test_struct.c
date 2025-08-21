#include <stdio.h>

struct foo {
	int a;
	short b;
	int c;
};

struct bar {
	int x;
	int y;
	short z;
};

typedef struct baz {
	char *name;
	int age;
	double money;
} baz_t;

typedef struct baz_2 {
	char* name;
	int age;
	double money;
} baz_2_t;

int main(int argc, char *argv[])
{
	printf("sizeof(foo) = %ld\n"
	       "sizeof(bar) = %ld\n"
	       "sizeof(baz) = %ld\n"
	       "sizeof(baz_2) = %ld\n",
	       sizeof(struct foo), sizeof(struct bar),
	       sizeof(struct baz), sizeof(struct baz_2));

	return 0;
}
