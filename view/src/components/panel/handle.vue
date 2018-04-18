<template>
  <div class="uk-article">
    <h3>Panel</h3>
    <h4>Status</h4>
    <handle-status
        :spider="spider"
        ref="handleStatus"
        @updateDownloadList='updateDownloadList'></handle-status>

    <h4>Crawl Data</h4>
    <handle-download
        :downloadList="downloadList" :spider="spider"
        @queryDownloadList='queryDownloadList' @updatePreviewData="updatePreviewData"></handle-download>

    <h4 v-if="previewData.length > 0">Preview</h4>
    <handle-preview v-if="previewData.length > 0" :previewData="previewData"></handle-preview>
  </div>
</template>

<script>
import handleStatus from './handleStatus'
import handleDownload from './handleDownload'
import handlePreview from './handlePreview'

export default {
  name: 'handle',
  data: function () {
    return {
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
    }
  },

  methods: {
    queryDownloadList: function () {
      this.$refs.handleStatus.updateDownloadList()
    },
    updateDownloadList: function (data) {
      this.downloadList = data
    },
    updatePreviewData: function (data) {
      this.previewData = data
    }
  }
}

</script>

<style scoped>

</style>
