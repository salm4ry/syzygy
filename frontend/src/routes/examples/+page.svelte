<svelte:head>
	<title>Examples | syzygy</title>
</svelte:head>

<script lang="ts">
import '../../app.css';

import Syzygy from '$lib/Syzygy.svelte';
import { examples } from './examples';

let selected = examples[0];

</script>

<article class="prose m-2 max-w-full">
<h1>Examples</h1>
<p>Visualise some example <span class="code">struct</span>s!</p>
<hr>
</article>

<div role="tablist" class="tabs tabs-border">
{#each examples as e}
<input type="radio" class="tab" value={e.name} bind:group={selected.name} aria-label="{e.name}">
<div class="tab-content bg-base-100 p-6">
    <p class="mb-4">{@html e.description}</p>
    <Syzygy bind:code={e.code}/>
</div>
{/each}
</div>
