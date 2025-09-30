<script lang="ts">
import {
	PUBLIC_FLASK_HOST,
	PUBLIC_FLASK_PORT
} from '$env/static/public';

export let data;
export let code: string;

async function submitCode(event: Event) {
	const form = event.target as HTMLFormElement;
	const code = new FormData(form).get("code") as string;

	// submit code to Flask server (retrieve host and port from environment
	try {
		const response = await fetch(
		`${PUBLIC_FLASK_HOST}:${PUBLIC_FLASK_PORT}/view`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ code: code })
		});

		// get response from Flask server
		data = await response.json();
	} catch (NetworkError) {
		data = [];
	}
}
</script>

<style>
textarea {
	min-height: 20rem;
	field-sizing: content;
	padding: 0.5em 1em;
}

::placeholder {
	color: #a5adce;  /* Catppuccin Macchiato subtext0 */
}
</style>

<form method="POST" on:submit|preventDefault={submitCode}>
	<textarea name="code"
		  placeholder="your code here"
		  class="textarea code bg-base-200 w-full h-full"
		  tabIndex={-1}
		  bind:value={code}></textarea>
	<button class="btn btn-primary mt-4">
		submit
	</button>
</form>
