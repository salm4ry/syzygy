<script lang="ts">
import { onMount } from "svelte";
import { accentColours as accentColours, paddingColour, borderColour } from "$lib/colours";

interface Rect {
	x: number,
	y: number,
	width: number,
	height: string,
	fill: string
};

let memberColours = accentColours;

const strokeWidth = 0.1;
const rectHeight = "50%";

// take JSON data from server as input
let { jsonData } = $props();
let svgData = $derived(buildSvg());  // SVG data derived from JSON data in buildSvg() function

function buildSvg() {
	let currentPos = 0;
	let res: Array<Rect> = [];

	for (const member of jsonData.members) {
		res = [...res, {
			x: currentPos,
			y: 0,
			width: member.size,
			height: rectHeight,
			fill: memberColours[currentPos % memberColours.length]
		}];

		currentPos += member.size;

		if (member.size < jsonData.alignment) {
			let extra = jsonData.alignment - member.size;

			res = [...res, {
				x: currentPos,
				y: 0,
				width: 0,
				height: rectHeight,
				fill: borderColour
			}];

			res = [...res, {
				x: currentPos,
				y: 0,
				width: extra,
				height: rectHeight,
				fill: paddingColour
			}];

			currentPos += extra;
		}

	}

	return {entries: res, totalWidth: currentPos};
}

onMount(() => {
	/*
	shuffle accent colour order (Fisher-Yates shuffle/Knuth shuffle): https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle#JavaScript_implementation

	determine the next element in the shuffled list by randomly drawing
	an element until no elements remain (here, by going through the array
	backwards)
	*/
	for (let i = memberColours.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i+1));
		[memberColours[i], memberColours[j]] = [
		memberColours[j], memberColours[i]];
	}

	buildSvg();
});
</script>

<style>
.card-title {
	font-family: 'Roboto Mono', monospace;
}

.struct {
	font-family: 'Roboto Mono', monospace;
	font-weight: normal;
}
</style>

<div class="card bg-base-300">
	<h2 class="card-title m-2"><span class="struct">struct</span> {jsonData.name}</h2>
	<p class="ml-2"><strong>size:</strong> {jsonData.size}</p>
	<p class="ml-2"><strong>alignment:</strong> {jsonData.alignment}</p>
	<!-- TODO scale SVG to fit in box -->
	<div class="center">
		<svg class="m-2" height="auto" width="100%"
			viewBox="0 0 {svgData.totalWidth} 5">
		{#each svgData.entries as s}
			{#if s.fill == borderColour}
				<!-- border between member bytes and their padding -->
				<line x1={s.x} x2={s.x} y1=0 y2={s.height}
					style="stroke-width:{strokeWidth};stroke:{borderColour}"/>
			{:else}
				<rect x={s.x} y={s.y} width={s.width} height={s.height}
				      style="fill:{s.fill}"/>
				{#if s.fill != paddingColour}
					<!-- border between struct members -->
					<line x1={s.x} x2={s.x} y1=0 y2={s.height}
						style="stroke-width:{strokeWidth};stroke:{borderColour}"/>
				{/if}
			{/if}
		{/each}
		</svg>
	</div>
</div>
