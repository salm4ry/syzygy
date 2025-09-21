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
	char **double_name;
	struct baz before;
	int age;
	double money;
} baz_2_t;

struct foobar {
	int a;
	char b;
	double c;
};

int main(int argc, char *argv[])
{
	printf("sizeof(foo) = %ld\n"
	       "sizeof(bar) = %ld\n"
	       "sizeof(baz) = %ld\n"
	       "sizeof(baz_2) = %ld\n"
	       "sizeof(foobar) = %ld\n",
	       sizeof(struct foo), sizeof(struct bar),
	       sizeof(struct baz), sizeof(struct baz_2),
	       sizeof(struct foobar));

	return 0;
}
