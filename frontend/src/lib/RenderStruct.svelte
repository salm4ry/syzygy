<script lang="ts">
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
	height: number,
	member: MemberInfo
};


const strokeWidth = 0.3;
const rectHeight = 50;

const emptyMember = {
	name: '',
	isPadding: true,
	size: 0,
	alignment: 0,
	colour: borderColour
};

// take JSON data from server as input
let { jsonData } = $props();
let svgData = $derived(buildSvg());  // SVG data derived from JSON data in buildSvg() function

let tooltipContent: MemberInfo = $state(emptyMember);

let colours = accentColours;

function genRandColour() {
	// refill colour array if it becomes empty
	if (colours.length == 0) {
		colours = accentColours;
	}

	// seed chosen by implementation
	let chosenColour = colours[Math.floor(Math.random()
		* colours.length)];

	// remove chosen colour in order to avoid collisions
	colours = colours.filter(
		item => item !== chosenColour
	);

	return chosenColour;
}

function buildBorder(position: number) {
	return {
		x: position,
		y: 0,
		height: rectHeight,
		member: emptyMember
	}
}

function buildRect(position: number, member: any) {
	return {
		x: position,
		y: 0,
		height: rectHeight,
		member: {
			name: member.name,
			isPadding: false,
			size: member.size,
			alignment: member.alignment,
			colour: genRandColour()
		}
	}
}

function buildPadding(position: number, width: number) {
	return {
		x: position,
		y: 0,
		height: rectHeight,
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

	for (const member of jsonData.members) {
		if (bytePos % member.alignment != 0) {
			// calculate padding size
			padding = member.alignment - (bytePos % member.alignment);

			// add border
			res = [...res, buildBorder(bytePos)];

			// add padding rectangle
			res = [...res, buildPadding(bytePos, padding)];
			bytePos += padding;
		}

		// add member border
		res = [...res, buildBorder(bytePos)];

		// add member rectangle
		res = [...res, buildRect(bytePos, member)];

		bytePos += member.size;
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
</script>

<div class="card bg-base-300">
	<h2 class="card-title code m-2"><span class="code font-normal">struct</span> {jsonData.name}</h2>
	<p class="ml-2"><strong>size:</strong> {jsonData.size}</p>
	<p class="ml-2"><strong>alignment:</strong> {jsonData.alignment}</p>

	<!-- spacing for tooltip -->
	<div class="pb-20"></div>
		<div class="tooltip" style="--tt-bg: {tooltipContent.colour}">
			<div class="tooltip-content flex flex-col items-start">
				{#if tooltipContent.name == ''}
					<p>click/hover over members for more information!</p>
				{:else}
					{#if tooltipContent.isPadding}
						<p><strong>padding</strong></p>
					{:else}
						<p><strong>name:</strong> <span class="code">{tooltipContent.name}</span></p>
					{/if}
					<p><strong>size:</strong> <span class="code">{tooltipContent.size}</span></p>
					{#if tooltipContent.alignment != 0}
						<p><strong>alignment:</strong> <span class="code">{tooltipContent.alignment}</span></p>
					{/if}
				{/if}
			</div>
			<svg class="p-4 w-full center !w-full" viewBox="0 0 {svgData.totalWidth} {svgData.totalWidth/5}"
			      preserveAspectRatio="none">
			{#each svgData.entries as s}
				{#if s.member.colour == borderColour}
					<!-- border between member bytes and their padding -->
					<line x1={s.x} x2={s.x} y1=0 y2={s.height}
						style="stroke-width:{strokeWidth};stroke:{borderColour}"/>
				{:else}
					<rect x={s.x} y={s.y} width={s.member.size} height={s.height}
					      style="fill:{s.member.colour}"
					      onmousemove={() => showTooltip(s.member)}
					      onfocus={() => showTooltip(s.member)}
					      onmouseout={() => hideTooltip()}
					      onblur={() => hideTooltip()}
					      role="tooltip">
					</rect>
				{/if}
			{/each}
			</svg>
		</div>
</div>
