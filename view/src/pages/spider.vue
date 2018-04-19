<template>
  <div class="uk-overflow-auto uk-height-1-1">

    <h3 class="uk-heading-bullet">{{status}}</h3>

    <p class="uk-text-bottom" v-if="status == 'Add'">
      Existed Spider? Go and
      <router-link to="/search" class="uk-link-text uk-text-primary">Search
        <span uk-icon="icon: search;ratio: 0.75;"></span>
      </router-link>
    </p>

    <spider-form
        :status="status" :spiderOnFocus="spider"></spider-form>
  </div>
</template>

<script>
import spiderForm from '../components/spider/spiderForm'

export default {
  name: 'spider',
  data: function () {
    return {
      status: (this.$route.query.mode ? this.$route.query.mode : 'Add')
    }
  },
  props: ['spider'],
  components: {
    spiderForm
  }
}

</script>

<style scoped>
  .uk-overflow-auto {
    border-top: #FFA72A 3px solid;
  }
</style>
