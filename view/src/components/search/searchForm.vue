<template>
  <div uk-margin>
    <div class="uk-search uk-search-navbar">
      <span uk-search-icon></span>
      <input v-model.lazy.trim="searchMeta" type="search" class="uk-search-input" placeholder="Search Spider...">
    </div>
    <div>
      <!-- paging -->
      <ul class="uk-pagination uk-flex uk-flex-right uk-margin-medium-bottom" uk-margin>

        <li v-show="querying">
          <span>
            <span uk-spinner></span> Querying...</span>
        </li>

        <li v-if="index > 1">
          <a @click="index -= 1">
            <span uk-pagination-previous></span>
          </a>
        </li>

        <li>{{index}}</li>
        <li>-</li>
        <li>{{length}}</li>

        <li v-if="index != length">
          <a @click="index += 1">
            <span uk-pagination-next></span>
          </a>
        </li>
      </ul>
    </div>
    <div v-if="empty && !querying" class="uk-margin-small">
      <span class="uk-meta">Find Nothing</span>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Qs from 'qs'

import util from '@/assets/util'

export default {
  name: 'search-form',
  data () {
    return {
      searchMeta: (this.$route.query.searchMeta ? this.$route.query.searchMeta : ''),
      index: 1,
      length: 1,
      querying: false,
      empty: false,
      url: util.apiUrl
    }
  },

  watch: {
    searchMeta: function () {
      this.index === 1 ? this.ajaxQuery() : this.index = 1
    },
    index: function () {
      this.ajaxQuery()
    }
  },

  created: function () {
    this.ajaxQuery()
  },

  methods: {
    ajaxQuery: function () {
      this.querying = true

      axios({
        method: 'POST',
        url: this.url + '/searchSpider',
        data: Qs.stringify({
          search: this.searchMeta,
          skip: (this.index - 1) * 3
        }),
        header: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
        .catch(err => {
          this.querying = false
          util.notification(err)
        })
        .then(response => {
          this.querying = false
          let msg = response.data
          let length = parseInt(msg['data']['length'] / 3)

          this.empty = (msg['data']['result'].length === 0)

          this.length = (msg['data']['length'] % 3 ? length + 1 : length)
          this.$emit('getSearchResults', msg['data']['result'])
        })
    }
  }
}

</script>

<style scoped>
  .uk-search-navbar {
    background-color: hsl(210, 9%, 96%);
    padding: 10px 0;
  }

</style>
