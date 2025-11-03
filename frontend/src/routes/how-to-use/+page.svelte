<svelte:head>
	<title>How to Use | syzygy</title>
</svelte:head>

<script lang="ts">
import '../../app.css';
import { typeEntries } from './typeEntries';

import { accentColours, paddingColour } from '$lib/colours';
</script>

<article class="prose m-2 mb-4 max-w-2/3">
<h1>How to Use</h1>

<p><strong class="text-primary">syzygy</strong> is a tool to visualise the memory layout of C
<span class="code">struct</span>s. Simply paste in your <span
class="code">struct</span> definitions, hit <strong
class="text-primary">submit</strong>, and watch the magic
happen!</p>


<h2>Colour Code</h2>
<ul>
	<li><span class="code">struct</span> members:
	{#each accentColours as colour}
		<span class="badge badge-xs" style="background-color: {colour}"></span>
	{/each}
	</li>

	<li>padding bytes:
	<span class="badge badge-xs" style="background-color: {paddingColour}"></span>
	</li>
</ul>

<h2>Supported Types</h2>

<div role="alert" class="alert alert-warning alert-soft">
<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 shrink-0 stroke-current" fill="none" viewBox="0 0 24 24">
<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
</svg>
<div class="test">syzygy does <span class="font-bold">not</span> support types defined with <span
class="code">typedef</span>: use the <span class="code">struct</span> name or
original type name</div>
</div>

<p class="mb-2">
	See the
	<a href="https://docs.python.org/3/library/ctypes.html#fundamental-data-types"
	   class="link link-primary" target="_blank">
		<span class="code">ctypes</span> documentation
	</a>
	for more information.
</p>

<ul>
	<li><span class="code font-bold">x</span> represents a number of bits (8, 16, 32, 64)</li>
	<li><span class="T font-bold">T</span> represents a type</li>
</ul>

<div class="overflow-x-auto rounded-box border border-base-content/5">
	<table class="table table-zebra mt-0 mb-0">
		<thead class="bg-primary/10">
			<tr>
				<th class="text-primary pl-2 font-bold">Category</th>
				<th class="text-primary font-bold">Types</th>
			</tr>
		</thead>
		<tbody>
		{#each typeEntries as entry}
			<tr>
				<td class="pl-2">{entry.category}</td>
				<td>
					<!-- responsive list:
					- two columns if there are more than two types to display
					- always 1 column on smaller screens
					-->
					<ul class="grid
					lg:grid-cols-{Number(entry.types.length > 2) + 1}">
						{#each entry.types as type}
						<li class="code">{type}</li>
						{/each}
					</ul>
				</td>
			</tr>
		{/each}
		</tbody>
	</table>
</div>

</article>
