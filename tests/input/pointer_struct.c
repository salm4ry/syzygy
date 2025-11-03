typedef struct pointer_struct {
	char *name;
	int age;
	double money;
} pointer_struct_t;

typedef struct large_pointer_struct {
	char* name;
	char **double_name;
	struct pointer_struct prev;
	int age;
	double money;
} large_pointer_struct_t;
