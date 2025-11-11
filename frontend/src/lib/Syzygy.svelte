<script lang="ts">
import "../app.css";

import CodeInput from "$lib/CodeInput.svelte";
import RenderStruct from "$lib/RenderStruct.svelte";
import ErrorAlert from "./ErrorAlert.svelte";

let data: JSON;
export let code: string;
</script>

<div class="w-90% h-90%">
	<div class="grid md:grid-cols-2 sm:grid-cols-1 gap-4">
		<div class="col-span-1">
			<CodeInput bind:data bind:code/>
		</div>
		<!-- split json array into individual elements and iterate over it -->
		<div class="col-span-1 grid grid-cols-1 gap-2">
			{#if data}
				{#if Object.keys(data).length != 0}
					{#each Object.entries(data) as entry}
						<!-- trim leading index -->
						{#if entry[1].hasOwnProperty('size')}
							<RenderStruct jsonData={entry[1]}/>
						{:else}
						<!-- TODO: differentiate between
						     empty response and no
						     response (i.e. backend down -->
						<ErrorAlert msg="Invalid struct <span class='code'>{entry[1].name}</span>"/>
						{/if}
					{/each}
				{:else}
					<ErrorAlert msg="Invalid struct(s)"/>
				{/if}
			{:else}
				<!-- no struct data to display: placeholder -->
				<div class="card bg-base-300 h-full p-2">
				</div>
			{/if}
		</div>
	</div>
</div>
