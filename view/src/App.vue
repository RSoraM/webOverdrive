<template>
  <div id="wo">
    <div class="uk-grid-small" uk-grid>

      <!-- Nav PC -->
      <div id="wo-1-4" class="uk-width-1-5 uk-visible@m">
        <nav-medium class="uk-padding"></nav-medium>
      </div>

      <!-- Nav Mobile -->
      <div class="uk-width-1-1 uk-hidden@m">
        <nav-small uk-sticky></nav-small>
      </div>

      <!-- view -->
      <div class="uk-width-4-5@m">
        <div class="uk-grid-small uk-child-width-1-3@m" uk-grid>

          <!-- vue route -->
          <router-view id="wo-2-4" class="uk-padding" :spider='spider' @spiderOnFocus='spiderOnFocus' />

          <!-- Detail PC -->
          <div id="wo-3-4" class="uk-padding uk-visible@m uk-panel uk-panel-scrollable">
            <detail v-if="!EmptySpider" :spider="spider"></detail>
          </div>

          <!-- Handle PC -->
          <div id="wo-4-4" class="uk-padding uk-visible@m uk-panel uk-panel-scrollable">
            <handle v-if="!EmptySpider" :spider="spider"></handle>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import navMedium from './components/nav/navMedium'
import navSmall from './components/nav/navSmall'
import handle from './components/panel/handle'
import detail from './components/panel/detail'

document.title = 'Web Overdrive'

export default {
  name: 'App',
  data: function () {
    return {
      spider: {}
    }
  },

  computed: {
    EmptySpider: function () {
      return !(Object.keys(this.spider).length > 0)
    }
  },

  components: {
    navMedium,
    navSmall,
    handle,
    detail
  },

  methods: {
    spiderOnFocus: function (item) {
      this.spider = item
    }
  }
}

</script>

<style>
  html,
  body {
    height: 100%;
    margin: 0px;
    padding: 0px;
  }

  #wo {
    height: 100%;
  }

  #wo-1-4,
  #wo-2-4,
  #wo-3-4,
  #wo-4-4 {
    height: 100vh;
  }

  @media screen and (max-width: 960px) {
    #wo-2-4 {
      height: calc(100vh - 95px);
    }
  }

  .uk-text-primary {
    color: #207394 !important;
  }

  .uk-text-danger {
    color: #EB4210 !important;
  }

  .uk-button-secondary {
    background-color: #FFA72A
  }

  .uk-button-secondary:hover {
    background-color: #DB9024
  }

  .uk-button-primary {
    background-color: #207394 !important;
    color: #ffffff !important;
  }

  .uk-button-primary:hover {
    background-color: #084152
  }

  .uk-button-danger {
    background-color: #EB4210;
  }

  .uk-button-danger:hover {
    background-color: #B22703
  }

</style>
