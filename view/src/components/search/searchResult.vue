<template>
  <div class="uk-card uk-card-default uk-card-body uk-card-small uk-margin-small uk-box-shadow-hover-large">
    <h4 class="uk-text-truncate">
      <a @click="spiderOnFocus(item)" class="uk-link-heading uk-visible@m">{{filteredSpider.name}}</a>
      <a @click="spiderOnFocus(item)" class="uk-link-heading uk-hidden@m" uk-switcher-item="next">{{filteredSpider.name}}</a>
    </h4>
    <p class="uk-text-truncate uk-text-meta">
      <span v-if="filteredSpider.description">
        {{filteredSpider.description}}
      </span>
      <span v-else>
        Missing Description.
      </span>
      <br>
      <span>
        items: {{filteredSpider.items.length}}
      </span>
    </p>
  </div>
</template>

<script>
export default {
  name: 'search-result',
  data: function () {
    return {}
  },
  props: ['item'],
  computed: {
    filteredSpider: function () {
      return this.item['spider']
    }
  },
  methods: {
    spiderOnFocus: function (spider) {
      this.$emit('spiderOnFocus', spider)
    }
  }
}

</script>

<style scoped>

</style>
