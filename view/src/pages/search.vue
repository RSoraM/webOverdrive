<template>
  <div class="uk-overflow-auto uk-height-1-1">
    <h3 class="uk-heading-bullet">Search</h3>
    <ul uk-switcher="connect: .searchSmall;" class="uk-tab uk-hidden@m">
      <li>
        <a href="">search</a>
      </li>
      <li v-if="width < 960">
        <a v-if="!EmptySpider" href="">detail</a>
      </li>
      <li v-if="width < 960">
        <a v-if="!EmptySpider" href="">Panel</a>
      </li>
    </ul>
    <ul class="uk-switcher searchSmall">
      <li>
        <search-form
            @getSearchResults='getSearchResults'></search-form>
        <search-result v-for="item in searchResult" v-bind:key="item.id" :item="item" @spiderOnFocus='spiderOnFocus'></search-result>
      </li>
      <li v-if="width < 960">
        <detail v-if="!EmptySpider" :spider="spider"></detail>
      </li>
      <li v-if="width < 960">
        <handle v-if="!EmptySpider" :spider="spider"></handle>
      </li>
    </ul>
  </div>
</template>

<script>
import searchForm from '../components/search/searchForm'
import searchResult from '../components/search/searchResult'
import detail from '../components/panel/detail'
import handle from '../components/panel/handle'

export default {
  name: 'search',
  data: function () {
    return {
      width: screen.width,
      searchResult: [],
      spider: {}
    }
  },

  computed: {
    EmptySpider: function () {
      return !(Object.keys(this.spider).length > 0)
    }
  },

  components: {
    searchForm,
    searchResult,
    detail,
    handle
  },

  methods: {
    getSearchResults: function (result) {
      this.searchResult = result
    },
    spiderOnFocus: function (spider) {
      this.spider = spider
      this.$emit('spiderOnFocus', spider)
    }
  }
}

</script>

<style scoped>
  .uk-overflow-auto {
    border-top: #207394 3px solid;
  }

</style>
