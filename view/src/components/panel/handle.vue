<template>
  <div class="uk-article">
    <h3>Panel</h3>
    <h4>Status</h4>
    <handle-status
        :spider="spider" :downloadList="downloadList"
        @updateDownloadList='updateDownloadList'></handle-status>
    <h4>Crawl Data</h4>
    <handle-download
        :downloadList="downloadList" :spider="spider"
        @updateDownloadList='updateDownloadList' @updatePreviewData="updatePreviewData"></handle-download>
    <h4 v-if="previewData.length > 0">Preview</h4>
    <handle-preview v-if="previewData.length > 0" :previewData="previewData"></handle-preview>
  </div>
</template>

<script>
import axios from 'axios'
import Qs from 'qs'

import handleStatus from './handleStatus'
import handleDownload from './handleDownload'
import handlePreview from './handlePreview'

import util from '@/assets/util'

export default {
  name: 'handle',
  data: function () {
    return {
      url: util.apiUrl,
      downloadList: [],
      previewData: []
    }
  },
  props: ['spider'],

  components: {
    handleStatus,
    handleDownload,
    handlePreview
  },

  watch: {
    spider: function () {
      this.downloadList = []
      this.previewData = []
      this.updateDownloadList()
    }
  },

  created: function () {
    this.updateDownloadList()
  },

  methods: {
    updateDownloadList: function () {
      axios({
        method: 'POST',
        url: this.url + '/listCrawlData',
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
          let msg = response.data
          this.downloadList = msg['data']
        })
    },
    updatePreviewData: function (data) {
      this.previewData = data
    }
  }
}

</script>

<style scoped>

</style>
