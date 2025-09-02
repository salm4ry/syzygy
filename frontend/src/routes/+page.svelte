<script lang="ts">
import { onMount } from 'svelte';

let data: JSON;

onMount(async () => {
	const response = await fetch('http://localhost:8000/view')
	data = await response.json();
	console.log("data: ", data);
});
</script>

<h1>syzygy 🪐</h1>
<!--<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to
    read the documentation</p> -->

<p style="font-family: monospace;">{JSON.stringify(data)}</p>
