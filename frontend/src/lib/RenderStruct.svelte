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

const strokeWidth = 0.3;
const rectHeight = "100%";

// take JSON data from server as input
let { jsonData } = $props();
let svgData = $derived(buildSvg());  // SVG data derived from JSON data in buildSvg() function

function buildBorder(position: number) {
	return {
		x: position,
		y: 0,
		width: 0,
		height: rectHeight,
		fill: borderColour
	}
}

function buildRect(position: number, memberIndex: number, width: number) {
	return {
		x: position,
		y: 0,
		width: width,
		height: rectHeight,
		fill: memberColours[memberIndex % memberColours.length]
	}
}

function buildPadding(position: number, width: number) {
	return {
		x: position,
		y: 0,
		width: width,
		height: rectHeight,
		fill: paddingColour
	}
}

function buildSvg() {
	let bytePos = 0;
	let res: Array<Rect> = [];
	let padding = 0;

	for (let i = 0; i < jsonData.members.length; i++) {
		let currentMember = jsonData.members[i];
		if (bytePos % currentMember.alignment != 0) {
			// calculate padding size
			padding = currentMember.alignment - (bytePos % currentMember.alignment);

			// add border
			res = [...res, buildBorder(bytePos)];

			// add padding rectangle
			res = [...res, buildPadding(bytePos, padding)];
			bytePos += padding;
		}

		// add member border
		res = [...res, buildBorder(bytePos)];

		// add member rectangle
		res = [...res, buildRect(bytePos, i, currentMember.size)];

		bytePos += currentMember.size;
	}

	if (bytePos % jsonData.alignment != 0) {
		padding = jsonData.alignment - (bytePos % jsonData.alignment);

		res = [...res, buildBorder(bytePos)];
		res = [...res, buildPadding(bytePos, padding)];

		bytePos += padding;
	}

	// final border
	res = [...res, buildBorder(bytePos)];

	console.assert(bytePos == jsonData.size,
		`expected struct size ${jsonData.size}, got ${bytePos}`);

	return {entries: res, totalWidth: jsonData.size};
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
		<svg class="m-2 w-48 w-full" viewBox="0 0 {svgData.totalWidth} {svgData.totalWidth/5}">
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
