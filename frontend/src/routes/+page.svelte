<script lang="ts">
import "../app.css";

import { onMount } from 'svelte';
import CodeInput from "$lib/CodeInput.svelte";

let data: JSON;
let code: string = "";

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
<!--
<div class="mockup-code w-full">
	<pre>{JSON.stringify(data, null, "\t")}</pre>
</div>
-->
</article>

<div class="w-90% h-90%">
	<div class="grid md:grid-cols-2 sm:grid-cols-1 gap-4">
		<div class="col-span-1">
			<form method="POST">
				<CodeInput bind:value={code}/>
				<button class="btn btn-primary mt-4">
					submit
				</button>
			</form>
			<button class="btn btn-error mt-4"
			onclick={() => console.log(code)}>
				get code value
			</button>
		</div>
		<div class="card bg-primary text-primary-content col-span-1">
			<p class="m-2">image here</p>
		</div>
	</div>
</div>
