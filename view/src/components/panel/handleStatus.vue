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
            <span v-html="lastedCrawl"></span>
          </td>
        </tr>
        <tr>
          <td>Status:</td>
          <td>
            <span v-html="status"></span>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="uk-margin" uk-margin>
      <label>
        <input v-model="advanceSetting" name="advanceSetting" type="checkbox" class="uk-checkbox"> Advance Setting
      </label>
      <div v-if="advanceSetting">
        <span>User-Agent:</span>
        <input v-model="setting.headers['user-agent']" type="text" class="uk-input" placeholder="User-Agent">
        <span>Delay:</span>
        <input v-model.number="setting.delay" type="number" class="uk-input" placeholder="Delay">
      </div>
    </div>

    <div v-if="status === 'Runable'" class="uk-child-width-1-1 uk-text-right" uk-grid>
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
    <div v-if="status === 'Running...'" class="uk-child-width-1-1 uk-text-right" uk-grid>
      <button class="uk-button uk-button-danger" @click="stopCrawl">Stop</button>
      <button class="uk-button uk-button-primary">Pause</button>
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
      advanceSetting: false,
      setting: {
        headers: {
          'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        },
        delay: 3
      },
      status: '<span uk-spinner></span> Querying...',
      lastedCrawl: '<span uk-spinner></span> Querying...'
    }
  },
  props: ['spider'],

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
    updateDownloadList: function () {
      this.lastedCrawl = '<span uk-spinner></span> Querying...'

      axios({
        method: 'POST',
        url: util.apiUrl + '/listCrawlData',
        data: Qs.stringify({
          id: this.spider.id
        }),
        header: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
        .catch(err => {
          this.lastedCrawl = 'ERR.'
          util.notification(err)
        })
        .then(response => {
          let msg = response.data
          if (msg['data'].length > 0) {
            this.lastedCrawl = msg['data'][0]['date']
          } else {
            this.lastedCrawl = 'Never run'
          }

          this.$emit('updateDownloadList', msg['data'])
        })
    },
    updateStatus: async function (isCall = false) {
      this.status = '<span uk-spinner></span> Querying...'

      if (!isCall) {
        this.updateDownloadList()
      }

      let count = 0
      do {
        await axios({
          method: 'POST',
          url: util.apiUrl + '/getStatus',
          data: Qs.stringify({
            id: this.spider.id
          }),
          header: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
          .catch(err => {
            this.status = 'ERR.'
            util.notification(err)
          })
          .then(response => {
            let message = response.data
            this.status = message['data']
          })

        if (!this.status) {
          this.status = 'ERR.'
          break
        }

        count++
        await this.sleep(3)
      } while (this.status !== 'Runable')

      if (count > 1) {
        this.updateDownloadList()
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
            let token = util.tokenStorage.fetch()
            axios({
              method: 'POST',
              url: util.apiUrl + '/rmSpider',
              data: Qs.stringify({
                id: that.spider.id,
                token: token
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
      let token = util.tokenStorage.fetch()

      axios({
        method: 'POST',
        url: util.apiUrl + '/crawlData',
        data: Qs.stringify({
          id: this.spider.id,
          setting: JSON.stringify(this.advanceSetting ? this.setting : {}),
          token: token
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
          this.updateStatus(true)
        })
    },
    stopCrawl: function () {
      let token = util.tokenStorage.fetch()

      axios({
        method: 'POST',
        url: util.apiUrl + '/stopCrawl',
        data: Qs.stringify({
          id: this.spider.id,
          token: token
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
          this.updateStatus(true)
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
