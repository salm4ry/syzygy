export const examples = [
{
	name: 'Simple struct',
	description: `Containing data types of different sizes (4, 2, and 1 bytes
		respectively)`,
	code:
`struct letters {
	int a;
	short b;
	char c;
};`,
}, {
	name: 'Struct dependency',
	description: `Here, the second <span class="code">struct</span> depends
		on the first i.e. uses the first within its definition. Note
		that syzygy can parse <span class="code">typedef</span>.`,
	code:
`typedef struct first {
	char *name;
	int age;
	double money;
} first_t;

typedef struct second {
	char **names;
	struct first old;
	int *ages;
	double bonus;
} second_t;`,
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
