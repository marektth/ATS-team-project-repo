<template>
  <div id="app">

    <nav class="navbar navbar-light bg-light">
      <div class="container-fluid">
        <button v-b-toggle.sidebar-no-header class="btn btn-outline"><b-icon icon="justify"></b-icon></button>
      </div>
    </nav>
    
    <div>
      <b-sidebar id="sidebar-no-header" aria-labelledby="sidebar-no-header-title" no-header shadow>
        <template #default="{ hide }">
          <div class="p-3">
            <h4 id="sidebar-no-header-title">Views</h4>
            <nav class="mb-3">
              <b-nav vertical>
                <b-nav-item>
                 <router-link to="/manager">Manager</router-link>
                </b-nav-item>
                <b-nav-item>
                  <router-link to="/">Employee</router-link> 
                </b-nav-item>
              </b-nav>
            </nav>
            <b-button variant="secondary" block @click="hide" size="sm">Close Sidebar</b-button>
          </div>
        </template>
      </b-sidebar>
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
