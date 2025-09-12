<script lang="ts">
import "../app.css";

import CodeInput from "$lib/CodeInput.svelte";
import RenderStruct from "$lib/RenderStruct.svelte";

let data: JSON;
</script>

<!-- TODO explain the application
<article class="prose">
</article>
-->

<div class="w-90% h-90%">
	<div class="grid md:grid-cols-2 sm:grid-cols-1 gap-4">
		<div class="col-span-1">
			<CodeInput bind:data/>
		</div>
		<!-- split json array into individual elements and iterate over it -->
		<div class="col-span-1 grid grid-cols-1 gap-2">
			{#if data}
				{#each Object.entries(data) as struct}
					<RenderStruct jsonData={struct}/>
				{/each}
			{:else}
				<!-- no struct data to display: placeholder -->
				<div class="card bg-base-300 h-full p-2">
				</div>
			{/if}
		</div>
	</div>
</div>
