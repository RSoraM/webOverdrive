<template>
  <div id="nav-medium" class="uk-overflow-auto uk-height-1-1">
    <h3 class=" uk-link-heading">
      <router-link to="/">WebOverdrive</router-link>
    </h3>
    <div class="uk-margin-large-top">
      <nav-option></nav-option>
    </div>
  </div>

</template>

<script>
import navOption from './navOption'

export default {
  name: 'nav-medium',
  data: function () {
    return {}
  },

  components: {
    navOption
  }
}

</script>

<style scoped>
  #nav-medium {
    height: 100vh;
  }

</style>
