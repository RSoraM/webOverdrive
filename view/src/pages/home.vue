<template>
  <div class="uk-section uk-section-small uk-flex uk-flex-middle uk-text-center">
    <div class="uk-width-1-1">
      <div class="uk-container">
        <p>
          <img src="@/assets/logo.png" alt="">
        </p>
        <p>
          A Python Crawler.
        </p>
        <router-link to="/spider" class="uk-button uk-button-secondary">Create</router-link>
        <router-link to="/search" class="uk-button uk-button-primary">search</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'home',
  data: function () {
    return {}
  }
}

</script>

<style scoped>
  img {
    width: 160px
  }

  .uk-section {
    border-top: #EB4210 3px solid;
  }

</style>
