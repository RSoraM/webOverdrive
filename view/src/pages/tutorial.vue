<template>
  <div class="uk-panel uk-panel-scrollable">
    <h3 class="uk-heading-bullet">Tutorial</h3>
    <div v-html="mdFile"></div>
  </div>
</template>

<script>
import axios from 'axios'

import util from '@/assets/util'

export default {
  name: 'tutorial',
  data: function () {
    return {
      mdFile: ''
    }
  },
  created: function () {
    let marked = require('marked')
    axios({
      method: 'GET',
      url: '/static/tutorial.md',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
      .catch(err => {
        util.notification(err)
      })
      .then(response => {
        let md = response.data
        this.mdFile = marked(md)
      })
  }
}

</script>

<style scoped>
  .uk-panel {
    border-top: #eb4210 3px solid;
  }

</style>
