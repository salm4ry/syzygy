<script lang="ts">
import "../app.css";
import { onMount } from 'svelte';

let data: JSON;

onMount(async () => {
	const response = await fetch('http://localhost:8000/view')
	data = await response.json();
	console.log("data: ", data);
});
</script>

<article class="prose">
<!--<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to
    read the documentation</p> -->

<!-- sample struct JSON information -->
<div class="mockup-code w-full">
	<pre>{JSON.stringify(data, null, "\t")}</pre>
</div>
</article>
