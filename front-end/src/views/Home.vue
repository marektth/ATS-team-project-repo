<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { apiService } from '../services/api'

export default Vue.extend({
  name: 'Home',
  components: {

  }, 
  methods: {
    async testLoad(){
      const api = new apiService();
      const request = await api.requestAllPeople();
      console.log(request.data)
    }
  },
  created() {
    this.testLoad()
  }
  
});
</script>
