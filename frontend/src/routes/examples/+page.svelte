<svelte:head>
	<title>Examples | syzygy</title>
</svelte:head>

<script lang="ts">
import '../../app.css';

import Syzygy from '$lib/Syzygy.svelte';
import { examples } from './examples';

let selected = examples[0].code;

</script>

<article class="prose m-2 max-w-full">
<h1>Examples</h1>
<p>Visualise some example <span class="code">struct</span>s!</p>
<hr>
</article>

<!-- TODO fix disappearing textarea on edit -->

<div role="tablist" class="tabs tabs-border">
{#each examples as e}
<label class="tab">
    <input type="radio" bind:group={selected} value={e.code}/>
    {e.name}
  </label>
<div class="tab-content bg-base-100 p-6">
    <p class="mb-4">{@html e.description}</p>
    <Syzygy bind:code={selected}/>
</div>
{/each}
</div>
