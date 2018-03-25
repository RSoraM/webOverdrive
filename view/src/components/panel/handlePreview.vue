<template>
  <ol>
    <li v-for="(data, index) in previewData" v-bind:key="index">
      <div class=" uk-overflow-auto">
        <table class="uk-table uk-table-small">
          <thead>
            <tr>
              <th>Item</th>
              <th>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(val, key) in data" v-bind:key="key">
              <td>{{key}}</td>
              <td>{{val}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </li>
  </ol>
</template>

<script>
export default {
  name: 'handle-preview',
  data: function () {
    return {}
  },
  props: ['previewData']
}

</script>

<style scoped>
  ol {
    border-top: 3px solid #FFA72A
  }

</style>
