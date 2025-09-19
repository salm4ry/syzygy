<script>
let { size, scaleFactor, svgData } = $props();

const borderColour = "#363a4f";  // surface0
</script>

<svg class="m-2" style:width={size} style:height={scaleFactor}>
	{#each svgData as s}
		<rect x={s.x} y={s.y} width={s.width} height={s.height}
		      style={`fill:${s.fill};stroke-width:2;stroke:${borderColour}`}/>
	{/each}
</svg>
