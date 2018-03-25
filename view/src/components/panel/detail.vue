<template>
  <article class="uk-article uk-text-meta">
    <h3>Spider Detail</h3>
    <h4>{{filteredSpider.name}}</h4>
    <span v-if="filteredSpider.description">
      {{filteredSpider.description}}
    </span>
    <span v-else>
      Missing Description.
    </span>

    <h4>URL:</h4>
    <a class="uk-link-heading" :href="filteredSpider.url" target="_blank">{{filteredSpider.url}}</a>

    <h4>ITEMS:</h4>
    <table class="uk-table uk-table-small">
      <thead>
        <tr>
          <th>name</th>
          <th>selector</th>
          <th>attr</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in filteredSpider.items" v-bind:key="index">
          <td>{{item.name}}</td>
          <td>{{item.selector}}</td>
          <td>{{item.attr}}</td>
        </tr>
      </tbody>
    </table>

    <h4>NEXT_PAGE_SELECTOR:</h4>
    <P v-if="filteredSpider.next">{{filteredSpider.next}}</P>
    <p v-else>None</p>
  </article>
</template>

<script>
export default {
  name: 'detail',
  data: function () {
    return {}
  },
  props: ['spider'],
  computed: {
    filteredSpider: function () {
      return this.spider.spider
    }
  }
}
</script>

<style scoped>
</style>
