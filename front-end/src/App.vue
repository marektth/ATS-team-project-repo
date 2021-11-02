<template>
  <div id="app">
    <nc-navbar variant="blue">
      <nc-navbar-list level="first">
        <nc-navbar-list-item title="ATS app" action="aaa" id="menuItem_001">
        </nc-navbar-list-item>
        <nc-list-group-item>
          <router-link to="/">Employee</router-link>
        </nc-list-group-item>
        <nc-list-group-item>
          <router-link to="/manager">Manager</router-link>
        </nc-list-group-item>
      </nc-navbar-list>
    </nc-navbar>
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
