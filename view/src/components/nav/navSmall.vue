<template>
  <div class="uk-width-1-1" id="nav-small">
    <nav class="uk-navbar-container uk-navbar-transparent" uk-navbar>
      <div class="uk-navbar-left">
        <router-link to="/" class="uk-navbar-item uk-logo">Web Overdrive</router-link>
      </div>
      <div class="uk-navbar-right">
        <ul class="uk-navbar-nav">
          <li>
            <a href="#nav-menu-small" uk-toggle uk-icon="icon: menu"></a>
            <nav-menu-small></nav-menu-small>
          </li>
        </ul>
      </div>
    </nav>
  </div>

</template>

<script>
import navMenuSmall from './navMenuSmall'

export default {
  name: 'nav-small',
  data: function () {
    return {}
  },
  components: {
    navMenuSmall
  }
}

</script>

<style scoped>

</style>
