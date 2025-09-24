<script>
import menu from '$lib/assets/menu.svg';
</script>

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
  <div class="navbar-start">
    <a class="btn btn-ghost text-xl text-primary" href="/">syzygy 🪐</a>
  </div>

  <div class="navbar-end">
    <div class="dropdown text-xl dropdown-end">
      <div tabindex="0" role="button" class="btn btn-ghost lg:hidden">
        <img src={menu} alt="Menubar icon"/>
      </div>
      <ul class="menu menu-sm dropdown-content bg-base-200 rounded-box z-1 mt-3 w-52 p-2 shadow">
        <li><a class="text-sm" href="/how-to-use">how to use</a></li>
	<li><a class="text-sm" href="/examples">examples</a></li>
	<li><a class="text-sm" href="/about">about</a></li>
      </ul>
    </div>
    <div class="hidden lg:flex">
      <ul class="menu menu-horizontal px-1">
        <li><a href="/how-to-use">how to use</a></li>
        <li><a href="/examples">examples</a></li>
        <li><a href="/about">about</a></li>
      </ul>
    </div>
  </div>

</div>
