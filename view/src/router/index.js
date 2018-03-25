import Vue from 'vue'
import Router from 'vue-router'
import route from './route'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: route
})
