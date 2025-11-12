<script lang="ts">
export let msg: string;
export let type: string;
</script>

<div role="alert" class="alert alert-error alert-soft alert-vertical sm:alert-horizontal">
	<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 shrink-0 stroke-current"
		fill="none" viewBox="0 0 24 24">
		    <path stroke-linecap="round" stroke-linejoin="round"
		    stroke-width="2"
			d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
		     />
	</svg>
	<!-- show different error messages depending on error type prop-->
	{#if type == "invalid"}
		{#if msg == ""}
			<p>Invalid struct(s)</p>
		{:else}
			<p>Invalid struct <span class="code">{msg}</span></p>
		{/if}
	{:else if type == "network"}
		<p>No response from server</p>
	{/if}
</div>

