import UIkit from 'uikit'
import api from './setting'

let SPIDER_STORAGE_KEY = 'wo-spider'
let TOKEN_STORAGE_KEY = 'wo-token'

export default {
  apiUrl: api,
  notification: function (message) {
    if (message.status === undefined) {
      UIkit.notification({
        message: message,
        pos: 'top-left',
        status: 'danger',
        timeout: 50000
      })
      return 0
    }
    if (message.status === 200) {
      UIkit.notification({
        message: message.message,
        status: 'success'
      })
    } else if (message.status > 200 && message.status < 500) {
      UIkit.notification({
        message: message.message,
        status: 'warning'
      })
    } else {
      UIkit.notification({
        message: message.message,
        status: 'danger'
      })
    }
  },
  spiderStorage: {
    fetch: function () {
      let empty = {
        name: '',
        description: '',
        url: '',
        items: [],
        next: ''
      }
      let spider = JSON.parse(
        localStorage.getItem(SPIDER_STORAGE_KEY) || JSON.stringify(empty)
      )
      return spider
    },
    save: function (spider) {
      localStorage.setItem(SPIDER_STORAGE_KEY, JSON.stringify(spider))
    }
  },
  tokenStorage: {
    fetch: function () {
      let token = localStorage.getItem(TOKEN_STORAGE_KEY) || ''
      return token
    },
    save: function (token) {
      localStorage.setItem(TOKEN_STORAGE_KEY, token)
    }
  }
}
