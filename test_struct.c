#include <stdio.h>
#include <stdbool.h>

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

struct array_test {
	int apple[4];
	bool banana[3];
	char cherry[2];
};

int main(int argc, char *argv[])
{
	printf("sizeof(foo) = %ld\n"
	       "sizeof(bar) = %ld\n"
	       "sizeof(baz) = %ld\n"
	       "sizeof(baz_2) = %ld\n"
	       "sizeof(foobar) = %ld\n"
	       "sizeof(array_test) = %ld\n",
	       sizeof(struct foo), sizeof(struct bar),
	       sizeof(struct baz), sizeof(struct baz_2),
	       sizeof(struct foobar), sizeof(struct array_test));

	return 0;
}
