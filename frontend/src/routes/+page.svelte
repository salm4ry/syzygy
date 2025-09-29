<svelte:head>
	<title>Home | syzygy</title>
</svelte:head>

<script lang="ts">
import "../app.css";

import Syzygy from "$lib/Syzygy.svelte";

let code: string;
</script>

<article class="prose m-2 mb-4">
<h1>welcome to syzygy 🪐</h1>

<blockquote>
In astronomy, a <strong class="text-primary">syzygy</strong> (/ˈsɪzədʒi/ SIZ-ə-jee; from Ancient Greek συζυγία (suzugía) 'union, yoking', expressing the sense of σύν (syn- "together") and ζυγ- (zug- "a yoke")) is a roughly straight-line configuration of three or more celestial bodies in a gravitational system.
</blockquote>
</article>

<Syzygy bind:code/>
