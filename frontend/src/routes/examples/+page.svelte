<svelte:head>
	<title>Examples | syzygy</title>
</svelte:head>

<script lang="ts">
import Syzygy from '$lib/Syzygy.svelte';
import '../../app.css';

// TODO separate examples array into own file and import
let examples = [{
name: 'Simple struct',
description: 'Containing data types of different sizes (4, 2, and 1 bytes\
	respectively)',
code: "struct letters {\n\
	int a;\n\
	short b;\n\
	char c;\n\
};",
}, {
name: 'Struct dependency',
description: 'Here, the second struct depends on the first i.e. uses the first\
	within its definition.',
code: "typedef struct baz {\n\
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
code: "struct fruits {\n\
	int apple[4];\n\
	bool banana[3];\n\
	char cherry[2];\n\
};"
},
];

export let selected = examples[0].code;

</script>

<article class="prose m-2 max-w-full">
<h1>Examples</h1>
<p>Visualise some example structs!</p>
<hr>
</article>

<div role="tablist" class="tabs tabs-border">
{#each examples as e}
<label class="tab">
    <input type="radio" bind:group={selected} value={e.code}/>
    {e.name}
  </label>
<div class="tab-content bg-base-100 p-6">
    <!-- TODO description -->
    <p class="mb-4">{e.description}</p>
    <Syzygy bind:code={selected}/>
</div>
{/each}
</div>
