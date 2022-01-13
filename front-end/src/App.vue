<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">ATS</a>
        <div class="collapse navbar-collapse" id="navbarText">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Employee</router-link> 
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/manager">Manager</router-link>
            </li>
          </ul>
          <span class="navbar-text" id="user-info">

          </span>
        </div>
      </div>
    </nav>

    <router-view/>
  </div>
</template>

<style>
html {
  font-size: 0.9rem;
}
#app {
  text-align: center;
}
</style>
