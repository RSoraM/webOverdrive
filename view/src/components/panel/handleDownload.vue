<template>
  <div>
    <select v-model="fileId" class="uk-select">
      <option v-for="file in downloadList" :key="file['id']" :value="file.id">{{file.date}}</option>
    </select>
    <div class=" uk-child-width-1-1 uk-text-right uk-margin-small" uk-grid>
      <div>
        <button class="uk-button uk-button-default">More</button>
        <div class="uk-text-left" uk-dropdown>
          <ul class="uk-nav uk-dropdown-nav">
            <li class="uk-nav-header">
              Download
            </li>
            <li>
              <a href="#" @click="downloadData('csv')">as .csv</a>
            </li>
            <li>
              <a href="#" @click="downloadData('json')">as .json</a>
            </li>
            <li class="uk-nav-divider"></li>
            <li>
              <a href="#" uk-toggle="target: #r-u-sure-file">Delete</a>
              <div id="r-u-sure-file" uk-modal>
                <div class="uk-modal-dialog">
                  <button class="uk-modal-close-default" type="button" uk-close></button>
                  <div class="uk-modal-header">
                    <h2 class="uk-modal-title">Are you Sure?</h2>
                  </div>
                  <div class="uk-modal-body">
                    <p>This Operation Will Delete This Crawl Data On Database.</p>
                    <p class="uk-text-right">
                      <button class="uk-button uk-button-danger uk-modal-close" type="button" @click="deleteData">Yes, I Do</button>
                      <button class="uk-button uk-button-primary uk-modal-close">No, Thanks</button>
                    </p>
                  </div>
                </div>
              </div>
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

import util from '@/assets/util'

export default {
  name: 'handle-download',
  data: function () {
    return {
      fileId: '',
      fileDate: '',
      token: util.tokenStorage.fetch(),
      url: util.apiUrl
    }
  },
  props: ['downloadList', 'spider'],
  computed: {
    filename: function () {
      if (this.fileId) {
        return this.spider['spider']['name'] + ' ' + this.fileDate
      }
      return undefined
    }
  },

  watch: {
    fileId: function () {
      this.fileDate = this.downloadList.find(item => {
        return item['id'] === this.fileId
      })['date']
    }
  },

  methods: {
    deleteData: function () {
      // form check
      if (!this.fileId) {
        let msg = {
          status: 500,
          message: 'Error: Select a file'
        }
        util.notification(msg)
        return 0
      }
      this.token = util.tokenStorage.fetch()

      axios({
        method: 'POST',
        url: this.url + '/rmCrawlData',
        data: Qs.stringify({
          id: this.fileId,
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
          let msg = response.data
          util.notification(msg)
          this.$emit('updateDownloadList')
        })
    },
    getData: async function () {
      let msg = {}
      await axios({
        method: 'POST',
        url: this.url + '/dlCrawlData',
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
          util.notification(msg)
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
