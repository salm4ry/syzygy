<script>
// take JSON data from server as input
let { jsonData } = $props();
</script>

<style>
.card {
	font-family: monospace;
}
</style>

<!-- TODO draw shapes
Basic SVG elements: https://datavisualizationwithsvelte.com/basics/basic-shapes
-->
<div class="card bg-base-300 col-span-1">
	<p class="m-2">{JSON.stringify(jsonData, null, "\t")}</p>
</div>
