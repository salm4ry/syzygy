<script lang="ts">
import "../app.css";

import CodeInput from "$lib/CodeInput.svelte";
import RenderStruct from "$lib/RenderStruct.svelte";

let data: JSON;
</script>

<style>
.center {
	margin: auto;  /* horizontally center */
	width: 50%;
}
</style>

<!-- TODO add memory layout colour code -->
<div class="center">
<article class="prose mb-4">
<h1>welcome to syzygy 🪐</h1>

<blockquote>
In astronomy, a <strong class="text-primary">syzygy</strong> (/ˈsɪzədʒi/ SIZ-ə-jee; from Ancient Greek συζυγία (suzugía) 'union, yoking', expressing the sense of σύν (syn- "together") and ζυγ- (zug- "a yoke")) is a roughly straight-line configuration of three or more celestial bodies in a gravitational system.
</blockquote>

<p><strong class="text-primary">syzygy</strong> is a tool to visualise the memory layout of C
structs. Simply paste in your code, hit <strong
class="text-primary">submit</strong>, and watch the magic
happen!</p>
</article>
</div>

<div class="w-90% h-90%">
	<div class="grid md:grid-cols-2 sm:grid-cols-1 gap-4">
		<div class="col-span-1">
			<CodeInput bind:data/>
		</div>
		<!-- split json array into individual elements and iterate over it -->
		<div class="col-span-1 grid grid-cols-1 gap-2">
			{#if data}
				{#each Object.entries(data) as entry}
					<!-- trim leading index -->
					<RenderStruct jsonData={entry[1]}/>
				{/each}
			{:else}
				<!-- no struct data to display: placeholder -->
				<div class="card bg-base-300 h-full p-2">
				</div>
			{/if}
		</div>
	</div>
</div>
