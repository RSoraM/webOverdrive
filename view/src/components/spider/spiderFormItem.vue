<template>
  <li uk-margin>
    <div>
      {
      <div>
        <div class=" uk-child-width-1-2 uk-grid uk-grid-small" uk-grid>
          <div>
            <input type="text" v-model.trim="item.name"
                class="uk-input uk-form-blank uk-form-small uk-margin-left uk-width-4-5" placeholder="Name"> :
          </div>
          <div>
            <input type="text" v-model.trim="item.selector"
                class="uk-input uk-form-blank uk-form-small" placeholder="CSS Selector">
          </div>
        </div>
        <div class=" uk-child-width-1-2 uk-grid uk-grid-small" uk-grid>
          <div>
            <input type="text"
                class="uk-input uk-disabled uk-form-blank uk-form-small uk-margin-left uk-width-4-5" placeholder="Attr"> :
          </div>
          <div>
            <input type="text" v-model.trim="item.attr"
                class="uk-input uk-form-blank uk-form-small" placeholder="text, href, src...">
          </div>
        </div>
      </div>
      },
      <a class="uk-icon-link uk-text-danger uk-text-small uk-margin-left" @click="emitItemNum()" uk-icon="icon: close; ratio: 0.75"></a>
    </div>
  </li>
</template>

<script>
export default {
  name: 'spider-form-item',
  props: [
    'item'
  ],
  data () {
    return {}
  },
  methods: {
    emitItemNum () {
      this.$emit('removeItem', this.item)
    }
  }
}

</script>

<style scoped>
  .uk-form-blank {
    background-color: hsl(210, 9%, 96%);
  }
  .uk-form-blank.uk-disabled{
    background-color: #ffffff;
  }
</style>
