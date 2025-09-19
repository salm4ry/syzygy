<script lang="ts">
import { onMount } from "svelte";

const scaleFactor = 10;

interface Rect {
	x: number,
	y: number,
	width: number,
	height: number,
	fill: string
};

// take JSON data from server as input
let { jsonData } = $props();
let svgData: Array<Rect> = $state([]);

onMount(() => {
	// define SVG data
	let currentPos = 0;

	for (const member of jsonData.members) {
		svgData = [...svgData, {
			x: currentPos * scaleFactor,
			y: 0,
			height: scaleFactor,
			width: member.size * scaleFactor,
			fill: "blue"
		}];

		currentPos += member.size;

		if (member.size < jsonData.alignment) {
			let extra = jsonData.alignment - member.size;

			// TODO remove magic constants
			svgData = [...svgData, {
				x: currentPos * scaleFactor,
				y: 0,
				height: scaleFactor,
				width: extra * scaleFactor,
				fill: "gray"
			}];

			currentPos += extra;
		}
	}
});
</script>

<style>
.card-title {
	font-family: 'Roboto Mono', monospace;
}
</style>

<div class="card bg-base-300">
	<h2 class="card-title m-2">{jsonData.name}</h2>
	<p class="m-2">alignment: {jsonData.alignment}</p>
	<!-- TODO scale SVG to fit in box -->
	<svg class="m-2" style:width={jsonData.size} style:height={scaleFactor}>
		{#each svgData as s}
			<rect x={s.x} y={s.y} width={s.width} height={s.height}
			      style={"fill:" + s.fill + ";stroke-width:0.2;stroke:black"}/>
		{/each}
	</svg>
</div>
