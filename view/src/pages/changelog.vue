<template>
  <div class="uk-panel uk-panel-scrollable">
    <h3 class="uk-heading-bullet">Change Log</h3>
    <div>
      <div v-for="(log, index) in logs" v-bind:key="index">
        <change-log-item :log="log"></change-log-item>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

import changeLogItem from '../components/changelog/changeLogItem'
import util from '@/assets/util'

export default {
  name: 'changelog',
  data: function () {
    return {
      logs: []
    }
  },
  components: {
    changeLogItem
  },
  created: function () {
    axios({
      method: 'GET',
      url: '/static/log.json',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
      .catch(err => {
        util.notification(err)
      })
      .then(response => {
        let msg = response.data
        this.logs = msg
      })
  }
}

</script>

<style scoped>
  .uk-panel {
    border-top: #ffa72a 3px solid;
  }

</style>
