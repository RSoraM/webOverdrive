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
            <span v-if="!querying">{{downloadList.length?downloadList[0].date:'Never run.'}}</span>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="uk-child-width-1-1 uk-text-right" uk-grid>
      <div>
        <span v-show="querying">
          <span uk-spinner></span> Crawling...
        </span>
      </div>
      <div class="uk-margin">
        <button class="uk-button uk-button-default">More</button>
        <div class="uk-text-left" uk-dropdown="mode: click">
          <ul class="uk-nav uk-dropdown-nav">
            <li class="uk-nav-header">
              Spider Operation
            </li>
            <li>
              <a href="#" @click="edit">Edit</a>
            </li>
            <li class="uk-nav-divider"></li>
            <li>
              <a href="#" @click="del">Delete</a>
            </li>
          </ul>
        </div>
        <button class="uk-button uk-button-primary" @click="crawl">Crawl</button>
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
  name: 'handle-run',
  data: function () {
    return {
      querying: false,
      token: util.tokenStorage.fetch(),
      url: util.apiUrl
    }
  },
  props: ['spider', 'downloadList'],
  methods: {
    edit: function () {
      this.$router.push({
        path: '/spider',
        query: {
          mode: 'Edit'
        }
      })
    },
    del: function () {
      let that = this
      UIkit.modal.confirm(
        '<h2 class="uk-modal-title">Are you Sure?</h2><p>This Operation Will Delete This Spider On Database.</p>'
      ).then(function () {
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
      }, function () {})
    },
    crawl: function () {
      this.token = util.tokenStorage.fetch()
      this.querying = true

      axios({
        method: 'POST',
        url: this.url + '/crawlData',
        timeout: 120 * 1000,
        data: Qs.stringify({
          id: this.spider.id,
          token: this.token
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
          let message = response.data

          util.notification(message)

          this.querying = false
          this.$emit('updateDownloadList')
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
