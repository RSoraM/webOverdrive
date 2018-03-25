<template>
  <div>
    <h4>Version {{log['message']}}</h4>
    <p class="uk-text-meta">{{log.date}}</p>
    <ul class="uk-list">
      <li v-for="(feed, index) in feeds" v-bind:key="index">
        <span :class="feedType(feed)"
            class="uk-label uk-margin-right uk-text-center">
          {{feed.type}}
        </span>
        {{feed.info}}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'

import util from '@/assets/util'

export default {
  name: 'change-log-item',
  data: function () {
    return {
      feeds: {}
    }
  },
  props: ['log'],
  created: function () {
    axios({
      method: 'GET',
      url: '/static/log/' + this.log['message'] + '.json',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
      .catch(err => {
        util.notification(err)
      })
      .then(response => {
        this.feeds = response.data
      })
  },
  methods: {
    feedType: function (feed) {
      switch (feed['type']) {
        case 'added':return 'uk-label-success'
        case 'fixed':return 'uk-label-danger'
        case 'changed':return ''
        case 'removed':return 'uk-label-warning'
        default:
          return ''
      }
    }
  }
}

</script>
