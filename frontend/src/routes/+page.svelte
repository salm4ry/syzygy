<script lang="ts">
import "../app.css";

import { onMount } from 'svelte';
import CodeInput from "$lib/CodeInput.svelte";

let data: JSON;
</script>

<style>
p {
    font-family: monospace;
}
</style>

<!-- TODO explain the application
<article class="prose">
</article>
-->

<div class="w-90% h-90%">
	<div class="grid md:grid-cols-2 sm:grid-cols-1 gap-4">
		<div class="col-span-1">
			<CodeInput bind:data/>
		</div>
		<div class="card bg-primary text-primary-content col-span-1">
			<p class="m-2">{JSON.stringify(data, null, "\t")}</p>
		</div>
	</div>
</div>
