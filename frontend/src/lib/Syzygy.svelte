<script lang="ts">
import "../app.css";

import { ERROR_RESP } from "$lib/error";
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
					<!-- check for designated error response
					     and use network error message if found -->
					{#if JSON.stringify(data) == JSON.stringify(ERROR_RESP)}
						<ErrorAlert msg="" type="network"/>
					{:else}
						{#each Object.entries(data) as entry}
							<!-- trim leading index -->
							{#if entry[1].hasOwnProperty('size')}
								<RenderStruct jsonData={entry[1]}/>
							{:else}
							<ErrorAlert msg={entry[1].name} type="invalid"/>
							{/if}
						{/each}
					{/if}
				{:else}
					<ErrorAlert msg="" type="invalid"/>
				{/if}
			{:else}
				<!-- no struct data to display: placeholder -->
				<div class="card bg-base-300 h-full p-2">
				</div>
			{/if}
		</div>
	</div>
</div>
