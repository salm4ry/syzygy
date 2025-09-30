export const examples = [
{
	name: 'Simple struct',
	description: 'Containing data types of different sizes (4, 2, and 1 bytes\
		respectively)',
	code:
`struct letters {
	int a;
	short b;
	char c;
};`,
}, {
	name: 'Struct dependency',
	description: 'Here, the second struct depends on the first i.e. uses the first\
		within its definition.',
	code:
`typedef struct baz {
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
} baz_2_t;`,
}, {
	name: 'Arrays',
	description: 'syzygy can handle arrays as well!',
	code:
`struct fruits {
	int apple[4];
	bool banana[3];
	char cherry[2];
};`
},
];
