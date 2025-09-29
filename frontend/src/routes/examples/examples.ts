export const examples = [
{
	name: 'Simple struct',
	description: 'Containing data types of different sizes (4, 2, and 1 bytes\
		respectively)',
	code:
"struct letters {\n\
	int a;\n\
	short b;\n\
	char c;\n\
};",
}, {
	name: 'Struct dependency',
	description: 'Here, the second struct depends on the first i.e. uses the first\
		within its definition.',
	code:
"typedef struct baz {\n\
	char *name;\n\
	int age;\n\
	double money;\n\
} baz_t;\n\
\n\
typedef struct baz_2 {\n\
	char* name;\n\
	char **double_name;\n\
	struct baz before;\n\
	int age;\n\
	double money;\n\
} baz_2_t;",
}, {
	name: 'Arrays',
	description: 'syzygy can handle arrays as well!',
	code:
"struct fruits {\n\
	int apple[4];\n\
	bool banana[3];\n\
	char cherry[2];\n\
};"
},
];
