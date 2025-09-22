<script lang="ts">
import { onMount } from "svelte";
import { accentColours as accentColours, paddingColour, borderColour } from "$lib/colours";

interface MemberInfo {
	name: string,
	isPadding: boolean,
	size: number,
	alignment: number,
	colour: string
}

interface Rect {
	x: number,
	y: number,
	height: string,
	fill: string
	member: MemberInfo
};


let memberColours = accentColours;

const strokeWidth = 0.3;
const rectHeight = "100%";

const emptyMember = {name: '', isPadding: true, size: 0, alignment: 0, colour: ''};

// take JSON data from server as input
let { jsonData } = $props();
let svgData = $derived(buildSvg());  // SVG data derived from JSON data in buildSvg() function

let tooltipContent: MemberInfo = $state(emptyMember);

function buildBorder(position: number) {
	return {
		x: position,
		y: 0,
		height: rectHeight,
		fill: borderColour,
		member: emptyMember
	}
}

function buildRect(position: number, memberIndex: number, member: any) {
	let colour = memberColours[memberIndex % memberColours.length];
	return {
		x: position,
		y: 0,
		height: rectHeight,
		fill: colour,
		member: {
			name: member.name,
			isPadding: false,
			size: member.size,
			alignment: member.alignment,
			colour: colour
		}
	}
}

function buildPadding(position: number, width: number) {
	return {
		x: position,
		y: 0,
		height: rectHeight,
		fill: paddingColour,
		member: {
			name: "padding",
			isPadding: true,
			size: width,
			alignment: 0,
			colour: paddingColour
		}
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
		res = [...res, buildRect(bytePos, i, currentMember)];

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

function showTooltip(content: MemberInfo) {
	tooltipContent = content;
}

function hideTooltip() {
  var tooltip = document.getElementById("tooltip");
  if (tooltip) {
	  tooltip.style.display = "none";
  }
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

<div class="card bg-base-300">
	<h2 class="card-title code m-2"><span class="code font-normal">struct</span> {jsonData.name}</h2>
	<p class="ml-2"><strong>size:</strong> {jsonData.size}</p>
	<p class="ml-2"><strong>alignment:</strong> {jsonData.alignment}</p>
	<div class="center">
		<div class="tooltip" style="--tt-bg: {tooltipContent.colour}">
			<div class="tooltip-content flex flex-col items-start">
				{#if tooltipContent.isPadding}
					<p><strong>padding</strong></p>
				{:else}
					<p><strong>name:</strong> <span class="code">{tooltipContent.name}</span></p>
				{/if}
				<p><strong>size:</strong> <span class="code">{tooltipContent.size}</span></p>
				{#if tooltipContent.alignment != 0}
					<p><strong>alignment:</strong> <span class="code">{tooltipContent.alignment}</span></p>
				{/if}
			</div>
			<svg class="m-2 w-48 w-full" viewBox="0 0 {svgData.totalWidth} {svgData.totalWidth/5}">
			{#each svgData.entries as s}
				{#if s.fill == borderColour}
					<!-- border between member bytes and their padding -->
					<line x1={s.x} x2={s.x} y1=0 y2={s.height}
						style="stroke-width:{strokeWidth};stroke:{borderColour}"/>
				{:else}
					<rect x={s.x} y={s.y} width={s.member.size} height={s.height}
					      style="fill:{s.fill}"
					      onmousemove={() => showTooltip(s.member)}
					      onfocus={() => showTooltip(s.member)}
					      onmouseout={() => hideTooltip()}
					      onblur={() => hideTooltip()}
					      role="tooltip">
					</rect>
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
</div>
