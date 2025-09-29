<svelte:head>
	<title>How to Use | syzygy</title>
</svelte:head>

<script lang="ts">
import '../../app.css';

import { accentColours, paddingColour } from '$lib/colours';
</script>

<article class="prose m-2 mb-4">
<h1>How to Use</h1>

<p><strong class="text-primary">syzygy</strong> is a tool to visualise the memory layout of C
structs. Simply paste in your code, hit <strong
class="text-primary">submit</strong>, and watch the magic
happen!</p>


<h2>Colour Code</h2>
<ul>
	<li>struct members:
	{#each accentColours as colour}
		<span class="badge badge-xs" style="background-color: {colour}"></span>
	{/each}
	</li>

	<li>padding bytes:
	<span class="badge badge-xs" style="background-color: {paddingColour}"></span>
	</li>
</ul>
</article>
