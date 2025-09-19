<script lang="ts">
import { onMount } from "svelte";
import StructImage from "./StructImage.svelte";

const scaleFactor = 10;

interface Rect {
	x: number,
	y: number,
	width: number,
	height: number,
	fill: string
};

// all accent colours except lavender (primary)
let accentColours = ["#f5bde6", "#c6a0f6", "#ed8796", "#ee99a0",
	"#f5a97f", "#eed49f", "#a6da95", "#8bd5ca",
	"#91d7e3", "#7dc4e4", "#8aadf4"];

const paddingColour = "#a5adcb";  // subtext0
const borderColour = "#363a4f";  // surface0

// take JSON data from server as input
let { jsonData } = $props();
let svgData: Array<Rect> = $state([]);

onMount(() => {
	// define SVG data
	let currentPos = 0;

	/*
	shuffle accent colour order (Fisher-Yates shuffle/Knuth shuffle): https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle#JavaScript_implementation

	determine the next element in the shuffled list by randomly drawing
	an element until no elements remain (here, by going through the array
	backwards)
	*/
	for (let i = accentColours.length - 1; i > 0; i--) {
		const j = Math.floor(Math.random() * (i+1));
		[accentColours[i], accentColours[j]] = [
		accentColours[j], accentColours[i]];
	}

	for (const member of jsonData.members) {
		svgData = [...svgData, {
			x: currentPos * scaleFactor,
			y: 0,
			height: scaleFactor,
			width: member.size * scaleFactor,
			fill: accentColours[currentPos % accentColours.length]
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
				fill: paddingColour
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
	<StructImage size={jsonData.size} scaleFactor={scaleFactor}
		svgData={svgData}/>
</div>
