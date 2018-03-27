<template>
  <div>
    <input type="text" v-model="i">
    <button @click="update">update</button>
    <br>
    i: {{i}}<br>
    o: {{o}}
    <br>
    <select v-model="selected">
      <option v-for="item in options" v-bind:value="item.value" v-bind:key="item.key">{{item.key}}</option>
    </select>
    {{selected}}
    <button @click="updateSel">update</button>
  </div>
</template>

<script>
export default {
  name: 'view-test',
  data: function () {
    return {
      options: [
        {key: 'a', value: '0'},
        {key: 'b', value: '1'},
        {key: 'c', value: '2'},
        {key: 'd', value: '3'}
      ],
      selected: '',
      i: '',
      o: ''
    }
  },
  methods: {
    update: function () {
      console.log(this.i)
      this.o = this.i
    },
    updateSel: function () {
      console.log(this.selected)
    }
  }
}

</script>

<style scoped>

</style>
