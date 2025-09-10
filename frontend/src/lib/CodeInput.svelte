<script>
export let value;
</script>

<style>
textarea {
	min-height: 20rem;
	field-sizing: content;
	padding: 0.5em 1em;
	font-family: monospace;
}
</style>

<textarea type="text"
	  placeholder="your code here"
	  class="textarea bg-base-200 w-full h-full"
	  bind:value>
</textarea>
