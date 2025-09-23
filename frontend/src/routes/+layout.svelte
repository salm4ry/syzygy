<script>
  import Navbar from "$lib/Navbar.svelte";

  let { children } = $props();
</script>

<Navbar />

<div class="m-4"></div>

<div class="p-2">
  {@render children()}
</div>
