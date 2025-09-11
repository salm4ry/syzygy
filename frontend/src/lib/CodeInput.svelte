<script lang="ts">
export let data;

async function submitCode(event: Event) {
	const form = event.target as HTMLFormElement;
	const code = new FormData(form).get("code") as string;

	// submit code to Flask server
	// TODO environment variable for port number?
	const response = await fetch('http://localhost:8000/view', {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({ code: code })
	});

	// get response from Flask server
	data = await response.json();
}
</script>

<style>
textarea {
	min-height: 20rem;
	field-sizing: content;
	padding: 0.5em 1em;
	font-family: monospace;
}

::placeholder {
	color: #a5adce;  /* Catppuccin Macchiato subtext0 */
}
</style>

<form method="POST" on:submit|preventDefault={submitCode}>
	<textarea name="code"
		  placeholder="your code here"
		  class="textarea bg-base-200 w-full h-full"
		  tabIndex={-1}></textarea>
	<button class="btn btn-primary mt-4">
		submit
	</button>
</form>
