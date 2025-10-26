<script>
  import Navbar from "$lib/Navbar.svelte";
  import Footer from "$lib/Footer.svelte";

  let { children } = $props();
</script>

<Navbar />

<div class="m-4"></div>

<div class="p-2">
  {@render children()}
</div>

<div class="m-4"></div>

<Footer/>
