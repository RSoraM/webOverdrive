<template>
  <div class="uk-text-small">
    <h4>Info:
      <span class="uk-text-danger">*</span>
    </h4>
    <div uk-margin>
      <input id="form-name" type="text" v-model.trim="spider.name" class="uk-input " placeholder="NAME">
      <textarea id='form-description' v-model.trim="spider.description" class="uk-textarea " placeholder="DESCRIPTION" rows="5"></textarea>
      <input id="form-url" type="text" v-model.trim="spider.url" class="uk-input " placeholder="URL">
    </div>

    <h4>Items:
      <span class="uk-text-danger">*</span>
      <button class="uk-button uk-button-primary uk-button-small" @click="addItem()">+</button>
    </h4>
    <ol id="form-items" uk-margin>
      <spider-form-item v-for="(item, index) in filteredItems" v-bind:key="index" :item="item" v-on:removeItem="rmItem"></spider-form-item>
    </ol>

    <h4>Others:</h4>
    <div uk-margin>
      <input id="form-next" type="text" v-model.trim="spider.next" class="uk-input uk-form-width-medium" placeholder="NEXT PAGE SELECTOR">
    </div>

    <hr>
    <div class="uk-text-right" uk-margin>
      <button class="uk-button uk-button-primary" @click="spiderOperate">{{status === 'Edit'?'Edit':'Create'}}</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Qs from 'qs'

import spiderFormItem from './spiderFormItem'
import util from '@/assets/util'

export default {
  name: 'spider-form',
  data () {
    return {
      spider: this.status === 'Edit' ? this.spiderOnFocus['spider'] : util.spiderStorage.fetch(),
      url: util.apiUrl,
      token: util.tokenStorage.fetch()
    }
  },
  props: ['status', 'spiderOnFocus'],

  components: {
    spiderFormItem
  },

  watch: {
    spider: {
      handler: function (spider) {
        util.spiderStorage.save(spider)
      },
      deep: true
    }
  },

  computed: {
    filteredItems: function () {
      let that = this
      if (this.spider.items.length === 0) {
        let item = {
          name: '',
          selector: '',
          attr: 'text'
        }
        that.spider.items.push(item)
      }
      return this.spider.items
    }
  },

  methods: {
    addItem () {
      if (this.spider.items.length < 10) {
        let tmp = {
          name: '',
          selector: '',
          attr: 'text'
        }
        this.spider.items.push(tmp)
      }
    },
    rmItem (item) {
      if (this.spider.items.length > 1) {
        this.spider.items.splice(this.spider.items.indexOf(item), 1)
      }
    },
    isIllegal: function (dic) {
      for (let name in dic) {
        if (!dic[name] && ['description', 'next'].indexOf(name) < 0) {
          return true
        } else if (typeof dic[name] === 'object') {
          for (let item in dic[name]) {
            if (this.isIllegal(dic[name][item])) {
              return true
            }
          }
        }
      }
      return false
    },
    spiderOperate () {
      this.token = util.tokenStorage.fetch()

      if (this.isIllegal(this.spider)) {
        let msg = {
          'status': 500,
          'message': 'Error: Illegal value'
        }
        util.notification(msg)
      } else {
        axios({
          method: 'POST',
          url: this.url + (this.status === 'Edit' ? '/editSpider' : '/addSpider'),
          data: Qs.stringify({
            spider: JSON.stringify(this.spider),
            token: this.token,
            id: Object.keys(this.spiderOnFocus).length > 0 ? this.spiderOnFocus['id'] : ''
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
            let that = this

            util.notification(msg)

            if (msg.status === 200) {
              that.$router.push({
                path: '/search'
              })
            }
          })
      }
    }
  }
}

</script>

<style scoped>
  .uk-form-blank {
    background-color: hsl(210, 9%, 96%);
  }

  ol {
    padding-left: 15px
  }

</style>
