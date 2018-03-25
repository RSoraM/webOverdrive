<template>
  <div uk-margin>
    <div class="uk-search uk-search-navbar">
      <span uk-search-icon></span>
      <input v-model.lazy.trim="searchMeta" type="search" class="uk-search-input" placeholder="Search Spider...">
    </div>
    <div v-show="querying">
      <span uk-spinner></span> Querying...
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
      querying: false,
      empty: false,
      url: util.apiUrl
    }
  },

  watch: {
    searchMeta: function () {
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
          search: this.searchMeta
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
          this.empty = (msg['data'].length === 0)

          this.$emit('getSearchResults', msg['data'])
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
