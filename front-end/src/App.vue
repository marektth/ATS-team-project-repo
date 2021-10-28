<template>
  <div id="app">
    <nc-navbar variant="blue">
      <nc-navbar-list level="first">
        <nc-navbar-list-item title="ATS app" action="aaa" id="menuItem_001">
        </nc-navbar-list-item>
      </nc-navbar-list>
    </nc-navbar>
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
#app {
  text-align: center;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #0a6cb3;
}
</style>
