import home from '../pages/home'
import spider from '../pages/spider'
import search from '../pages/search'
// import tutorial from '../pages/tutorial'
// import changelog from '../pages/changelog'
// import viewTest from '../pages/viewTest'

export default [
  {
    path: '/',
    name: 'Home',
    component: home
  },
  {
    path: '/spider',
    name: 'Spider',
    component: spider
  },
  {
    path: '/search',
    name: 'Search',
    component: search
  }
  // {
  //   path: '/tutorial',
  //   name: 'Tutorial',
  //   component: tutorial
  // },
  // {
  //   path: '/changelog',
  //   name: 'Change Log',
  //   component: changelog
  // }
  // {
  //   path: '/viewTest',
  //   name: 'view_test',
  //   component: viewTest
  // }
]
