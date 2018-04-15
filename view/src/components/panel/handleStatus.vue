<template>
  <div>
    <table class="uk-table uk-table-small uk-margin-remove uk-text-meta">
      <tbody>
        <tr>
          <td>Created Date:</td>
          <td>{{spider.createdDate}}</td>
        </tr>
        <tr>
          <td>Lasted Crawl:</td>
          <td>
            <span>{{downloadList.length?downloadList[0].date:'Never run.'}}</span>
          </td>
        </tr>
        <tr>
          <td>Status:</td>
          <td>
            <span v-show="running">
              <span uk-spinner></span> Running...
            </span>
            <span v-show="!running">
              Runable
            </span>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="uk-child-width-1-1 uk-text-right" uk-grid>
      <div class="uk-margin">
        <button class="uk-button uk-button-default">More</button>
        <div class="uk-text-left" uk-dropdown="mode: click">
          <ul class="uk-nav uk-dropdown-nav">
            <li class="uk-nav-header">
              Spider Operation
            </li>
            <li>
              <a href="#" @click="editSpider">Edit</a>
            </li>
            <li class="uk-nav-divider"></li>
            <li>
              <a href="#" @click="delSpider">Delete</a>
            </li>
          </ul>
        </div>
        <button class="uk-button uk-button-primary" @click="crawlData">Crawl</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Qs from 'qs'
import UIkit from 'uikit'

import util from '@/assets/util'

export default {
  name: 'handle-status',
  data: function () {
    return {
      running: false,
      token: util.tokenStorage.fetch(),
      url: util.apiUrl
    }
  },
  props: ['spider', 'downloadList'],

  created: function () {
    this.updateStatus()
  },

  watch: {
    spider: {
      handler: function () {
        this.updateStatus()
      },
      deep: true
    }
  },

  methods: {
    sleep: function (sec) {
      return new Promise(resolve => setTimeout(resolve, sec * 1000))
    },
    updateStatus: async function (isRec = false) {
      await axios({
        method: 'POST',
        url: this.url + '/getStatus',
        data: Qs.stringify({
          id: this.spider.id
        }),
        header: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
        .catch(err => {
          util.notification(err)
        })
        .then(response => {
          let message = response.data
          this.running = message['data']
        })

      if (this.running) {
        await this.sleep(3)
        await this.updateStatus(isRec = true)
      } else if (!this.running && isRec) {
        this.$emit('updateDownloadList')
      }
    },
    editSpider: function () {
      this.$router.push({
        path: '/spider',
        query: {
          mode: 'Edit'
        }
      })
    },
    delSpider: function () {
      let that = this
      UIkit.modal
        .confirm(
          `
          <h2 class="uk-modal-title">Are you Sure?</h2>
          <p>This Operation Will Delete This Spider On Database.</p>
          `
        )
        .then(
          function () {
            that.token = util.tokenStorage.fetch()
            axios({
              method: 'POST',
              url: that.url + '/rmSpider',
              data: Qs.stringify({
                id: that.spider.id,
                token: that.token
              }),
              header: {
                'Content-Type': 'application/x-www-form-urlencoded'
              }
            })
              .catch(err => {
                util.notification(err)
              })
              .then(response => {
                let message = response.data
                util.notification(message)
              })
          },
          function () {}
        )
    },
    crawlData: function () {
      this.token = util.tokenStorage.fetch()

      axios({
        method: 'POST',
        url: this.url + '/crawlData',
        data: Qs.stringify({
          id: this.spider.id,
          token: this.token
        }),
        header: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
        .catch(err => {
          util.notification(err)
        })
        .then(response => {
          let message = response.data

          util.notification(message)
          this.updateStatus()
        })
    }
  }
}

</script>

<style scoped>
td {
  padding-left: 0px;
  padding-right: 0px;
}
</style>
