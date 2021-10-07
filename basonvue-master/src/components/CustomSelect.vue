<template>
  <div class="custom-select" :tabindex="tabindex" @blur="open = false">
    <div class="selected" :class="{ open: open, disabled : isPlayingStore && name!=='filter'}" @click="openMenu">
      <div :id="id">
        {{ selected.substring(0,7)}}
      </div>
    </div>
    <div class="items" :class="{ selectHide: !open }">
      <div
        v-for="(option, i) of options"
        :key="i"
        @click="
          selected = option;
          open = false;
          $emit('input', option);
        "
      >
        {{ option.substring(0,numberOfLetters)}}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  computed:{
    isPlayingStore(){
      return this.$store.state.isPlaying;
    }
  },
  props: {
    options: {
      type: Array,
      required: true,
    },
    default: {
      type: String,
      required: false,
      default: null,
    },
    tabindex: {
      type: Number,
      required: false,
      default: 0,
    },
    isShown:{
      type: Boolean,
      required: false,
      default: true,
    },
    numberOfLetters:{
      type: Number,
      required: false,
      default: 7,
    },
    id:{
      type: String,
      required: false,
      default: "none" 
    }
  },
  data() {
    return {
      selected: this.default
        ? this.default
        : this.options.length > 0
        ? this.options[0]
        : null,
      open: false,
    };
  },
  methods:{
    openMenu(){
      if(!this.$store.state.isPlaying){
        this.open = !this.open;
      }
    }
  }
};
</script>

<style scoped>
.custom-select {
  position: relative;
  width: 100%;
  text-align: left;
  outline: none;
  height: 3rem;
  line-height: 3rem;
  box-sizing: border-box;
}

.custom-select .selected {
  background-color: #0a0a0a;
  border-radius: 6px;
  color: #fff;
  padding-left: 1em;
  cursor: pointer;
  user-select: none;
}

.custom-select .selected.open {
  border: 1px solid #666666;
  border-radius: 6px 6px 0px 0px;
}

.custom-select .selected:after {
  position: absolute;
  content: "";
  top: 50%;
  right: 1em;
  width: 0;
  height: 0;
  border: 5px solid transparent;
  border-color: #fff transparent transparent transparent;
}

.custom-select .items {
  color: #fff;
  border-radius: 0px 0px 6px 6px;
  border-right: 1px solid #666666;
  border-left: 1px solid #666666;
  border-bottom: 1px solid #666666;
  position: absolute;
  background-color: #0a0a0a;
  left: 0;
  right: 0;
  z-index: 1;
}

.custom-select .items div {
  color: #fff;
  padding-left: 1em;
  cursor: pointer;
  user-select: none;
}

.custom-select .items div:hover {
  background-color: #7e7e7e;
}

.selectHide {
  display: none;
}

.disabled{
  opacity: 0.5;
}


</style>
