<template>
  <ul class="uk-nav uk-nav-default uk-margin-auto-vertical">
    <li class="uk-nav-header">What about...</li>
    <li class="uk-nav-divider"></li>
    <router-link v-for="router in routers" tag="li" :to="router.path" exact-active-class="uk-active" :key="router.name">
      <a>{{router.name}}</a>
    </router-link>

    <li class="uk-nav-header uk-margin-large-top">Token</li>
    <li class="uk-nav-divider"></li>
    <li class="uk-margin-small">
      <input v-model.lazy.trim="token" type="text" class="uk-form-blank uk-input" placeholder="Enter your token">
    </li>
    <li class="uk-margin-small">
      <button @click="authToken" class="uk-button uk-button-primary uk-align-right">Auth</button>
    </li>
  </ul>
</template>

<script>
import axios from 'axios'
import Qs from 'qs'

import route from '@/router/route'

import util from '@/assets/util'

export default {
  name: 'nav-option',
  data: function () {
    return {
      routers: route,
      url: util.apiUrl,
      token: util.tokenStorage.fetch()
    }
  },

  watch: {
    token: {
      handler: function (token) {
        util.tokenStorage.save(token)
        this.authToken(token)
      },
      deep: true
    }
  },

  methods: {
    authToken: function () {
      this.token = util.tokenStorage.fetch()

      axios({
        method: 'POST',
        url: this.url + '/auth',
        data: Qs.stringify({
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
        })
    }
  }
}

</script>

<style scoped>
  .uk-form-blank {
    background-color: hsl(210, 9%, 96%);
  }
  @media screen and (max-width: 960px) {
    .uk-form-blank {
      background-color: inherit
    }
  }
</style>
