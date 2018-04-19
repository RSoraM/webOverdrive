<template>
  <div>
    <select v-model="fileId" class="uk-select">
      <option disabled value="">Select a file</option>
      <option v-for="file in downloadList" :key="file['id']" :value="file.id">{{file.date}}</option>
    </select>
    <div class=" uk-child-width-1-1 uk-text-right uk-margin-small" uk-grid>
      <div>
        <button class="uk-button uk-button-default">More</button>
        <div class="uk-text-left" uk-dropdown="mode: click">
          <ul class="uk-nav uk-dropdown-nav">
            <li class="uk-nav-header">Download</li>
            <li>
              <a href="#" @click="downloadData('csv')">as .csv</a>
            </li>
            <li>
              <a href="#" @click="downloadData('json')">as .json</a>
            </li>
            <li class="uk-nav-divider"></li>
            <li>
              <a href="#" @click="delData">Delete</a>
            </li>
          </ul>
        </div>
        <button class="uk-button uk-button-primary" @click="previewData">Preview</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Qs from 'qs'
import Papa from 'papaparse'
import UIkit from 'uikit'

import util from '@/assets/util'

export default {
  name: 'handle-download',
  data: function () {
    return {
      fileId: ''
    }
  },
  props: ['downloadList', 'spider'],

  computed: {
    filename: function () {
      let that = this
      if (this.fileId) {
        let fileDate = that.downloadList.find(item => {
          return item['id'] === that.fileId
        })['date']
        return this.spider['spider']['name'] + ' ' + fileDate
      }
      return undefined
    }
  },

  watch: {
    downloadList: {
      handler: function () {
        this.fileId = ''
      },
      deep: true
    }
  },

  methods: {
    delData: function () {
      let that = this

      UIkit.modal.confirm(
        '<h2 class="uk-modal-title">Are you Sure?</h2><p>This Operation Will Delete This Data On Database.</p>'
      ).then(function () {
        let token = util.tokenStorage.fetch()

        axios({
          method: 'POST',
          url: util.apiUrl + '/rmCrawlData',
          data: Qs.stringify({
            id: that.fileId,
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
            let msg = response.data
            util.notification(msg)
            that.$emit('updatePreviewData', [])
            that.$emit('queryDownloadList')
          })
      }, function () {})
    },
    getData: async function () {
      let msg = {}
      await axios({
        method: 'POST',
        url: util.apiUrl + '/dlCrawlData',
        data: Qs.stringify({
          id: this.fileId
        }),
        header: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
        .catch(err => {
          util.notification(err)
        })
        .then(response => {
          msg = response.data
        })

      return msg
    },
    toFile: function (content, filename) {
      let link = document.createElement('a')
      link.download = filename
      link.style.display = 'none'

      let blob = new Blob(['\ufeff' + content])
      link.href = URL.createObjectURL(blob)

      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    previewData: async function () {
      let msg = await this.getData()
      this.$emit('updatePreviewData', msg['data'])
    },
    downloadData: async function (fileTpye) {
      // form check
      if (!fileTpye || !this.fileId) {
        let msg = {
          status: 500,
          message: 'Error: Select a file'
        }
        util.notification(msg)
        return 0
      }

      let msg = await this.getData()
      let data = msg['data']

      if (fileTpye === 'csv') {
        let csv = Papa.unparse(JSON.stringify(data))
        this.toFile(csv, this.filename + '.' + fileTpye)
      } else if (fileTpye === 'json') {
        this.toFile(JSON.stringify(data, null, 2), this.filename + '.' + fileTpye)
      }
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
