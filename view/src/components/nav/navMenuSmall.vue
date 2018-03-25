<template>
  <div id="nav-menu-small" uk-offcanvas="mode: slide; overlay: true; flip: true">
    <div class="uk-offcanvas-bar uk-flex uk-flex-column">
      <button class="uk-offcanvas-close" type="button" uk-close></button>
      <nav-option></nav-option>
    </div>
  </div>
</template>

<script>
import navOption from './navOption'

export default {
  name: 'nav-menu-small',
  data: function () {
    return {}
  },

  components: {
    navOption
  }
}
</script>

<style scoped>

</style>
