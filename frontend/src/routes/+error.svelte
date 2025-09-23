<script>
import '../app.css';
import { page } from '$app/state';
</script>

<article class="prose mb-4">
	<h1><span class="text-primary">{page.status}</span> {page.error?.message}</h1>
</article>
