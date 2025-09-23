<style>
  /* stick to top of screen */
  .sticky {
      position: sticky;
      top: 0;
  }

  .btn {
      font-weight: 900;
  }
</style>

<!-- rounded-b: only round bottom -->
<div class="navbar sticky bg-base-300 shadow-sm rounded-b">

  <div class="flex-1">
    <a class="btn btn-ghost text-xl text-primary" href="/">syzygy 🪐</a>
  </div>

  <!-- TODO responsive: condense to drop-down on smaller screens -->
  <div class="flex-none">
    <ul class="menu menu-horizontal px-1">
      <li><a href="/how-to-use">how to use</a></li>
      <li><a href="/examples">examples</a></li>
      <li><a href="/about">about</a></li>
    </ul>
  </div>

</div>
