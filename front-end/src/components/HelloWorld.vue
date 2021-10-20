<template>
  <div class="hello">
    <nc-button variant="primary">Primary</nc-button>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  name: 'HelloWorld',
  props: {
    msg: String,
  },
});
</script>
