<template>
  <div class="home" style="padding-top:50px">
    <img :src="require('../assets/images/bg.jpg')"/>
    <Master />
    <div>
      <div class="channels mx-3">
        <span class="channels-label">CHANNELS</span>
        <div class="channels-body" id="channelSample">
          <Timebar />
          <div class="channels-bodyWithoutButton" style='margin-top: 1em'>
            <Channel v-for="sample in samplesChosen" v-bind:key="sample.id" :id="sample.id" :name="sample.name" :src="sample.src" class="channel-draggable"/>
          </div>
          <button type="button" class="btn btn-secondary shadow-none ms-1 buttonAddChannel" style="background-color:#888; margin-top:8px; color: ghostwhite; display: flex" @click="addChannel">
            <p style="margin: 10px 15px 0 0"> ADD CHANNEL</p>
            <svg viewBox="0 -47 354.98667 354" width="32" height="32" xmlns="http://www.w3.org/2000/svg" fill="white" style="margin-top: 3px;">
              <path d="m6.828125 102.894531c-3.773437 0-6.828125 3.054688-6.828125 6.824219v34.132812c0 3.773438 3.054688 6.828126 6.828125 6.828126 3.769531 0 
                       6.824219-3.054688 6.824219-6.828126v-34.132812c0-3.769531-3.054688-6.824219-6.824219-6.824219zm0 0"/>
              <path d="m40.984375 74.941406c-3.769531 0-6.828125 3.058594-6.828125 6.828125v94.515625c0 3.773438 3.058594 6.828125 6.828125 6.828125s6.828125-3.054687
                       6.828125-6.828125v-94.515625c0-3.769531-3.058594-6.828125-6.828125-6.828125zm0 0"/>
              <path d="m75.09375 27.800781c-3.769531 0-6.828125 3.054688-6.828125 6.824219v191.148438c0 3.769531 3.058594 6.828124 6.828125 6.828124s6.828125-3.058593
                       6.828125-6.828124v-191.148438c0-3.769531-3.058594-6.824219-6.828125-6.824219zm0 0"/>
              <path d="m109.226562 61.933594c-3.769531 0-6.828124 3.054687-6.828124 6.828125v116.050781c0 3.769531 3.058593 6.828125 6.828124 6.828125 3.769532 0
                       6.828126-3.058594 6.828126-6.828125v-116.050781c0-3.773438-3.058594-6.828125-6.828126-6.828125zm0 0"/>
              <path d="m212.292969 45.40625c-3.769531 0-6.824219 3.054688-6.824219 6.828125v153.589844c0 3.769531 3.054688 6.824219 6.824219 6.824219s6.828125-3.054688
                       6.828125-6.824219v-153.589844c0-3.773437-3.058594-6.828125-6.828125-6.828125zm0 0"/>
              <path d="m279.894531 55.105469c-3.769531 0-6.828125 3.058593-6.828125 6.828125v136.53125c0 3.773437 3.058594 6.828125 6.828125 6.828125s6.824219-3.054688 
                       6.824219-6.828125v-136.53125c0-3.769532-3.054688-6.828125-6.824219-6.828125zm0 0"/>
              <path d="m314.027344 89.238281c-3.769532 0-6.828125 3.058594-6.828125 6.828125v68.265625c0 3.769531 3.058593 6.828125 6.828125 6.828125 3.769531 0 
                       6.824218-3.058594 6.824218-6.828125v-68.265625c0-3.769531-3.054687-6.828125-6.824218-6.828125zm0 0"/>
              <path d="m245.761719.492188c-3.773438 0-6.828125 3.058593-6.828125 6.828124v245.757813c0 3.773437 3.054687 6.828125 6.828125 6.828125 3.769531 0 
                       6.824219-3.054688 6.824219-6.828125v-245.757813c0-3.769531-3.054688-6.828124-6.824219-6.828124zm0 0"/>
              <path d="m143.359375 109.71875c-3.769531 0-6.824219 3.058594-6.824219 6.828125v27.304687c0 3.773438 3.054688 6.828126 6.824219 6.828126s6.828125-3.054688 
                       6.828125-6.828126v-27.304687c0-3.769531-3.058594-6.828125-6.828125-6.828125zm0 0"/>
              <path d="m348.160156 107.433594c-3.769531 0-6.828125 3.054687-6.828125 6.824218v29.539063c0 3.769531 3.058594 6.828125 6.828125 6.828125 3.769532 0
                       6.828125-3.058594 6.828125-6.828125v-29.539063c0-3.769531-3.058593-6.824218-6.828125-6.824218zm0 0"/>
              <path d="m176.851562 94.417969c-3.773437 0-6.828124 3.054687-6.828124 6.824219v55.570312c0 3.769531 3.054687 6.828125 6.828124 6.828125 3.769532 0 
                       6.824219-3.058594 6.824219-6.828125v-55.570312c0-3.769532-3.054687-6.824219-6.824219-6.824219zm0 0"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Master from '@/components/Master.vue'
import Channel from '@/components/Channel.vue'
import Timebar from "@/components/Timebar.vue";
import { Sortable } from '@shopify/draggable';

export default {
  name: 'Sequencer',
  beforeCreate () {
    document.querySelector('body').setAttribute('style', 'min-width: 1700px')

  },
  components: {
    Master, Channel, Timebar
  },
  computed: {
    samplesChosen(){
      return this.$store.state.samplesChosen;
    },
    getAudioCtx(){
        return this.$store.getters.getAudioCtx;
    },
    /*waitKit(){
            if (this.$store.state.initWithKit) {
                this.$router.push('/');
            }
            else {
                setTimeout(this.waitKit, 10);
            }
        }*/
  },
  methods:{
    async addChannel(){
      /*var sourceURL = require('../assets/sounds/kick.wav');
      var blob = await this.fetchFile(sourceURL);
      var arrayBuffer = await this.readUploadedFile(blob);
      var audioBuffer = await this.createAudioBuffer(arrayBuffer);*/
      this.$store.commit('addSamplesChosen',{sampleName:"Default", src:/*audioBuffer*/null});
    },
    fetchFile(url){
      return new Promise((resolve, reject) => {
        fetch(url).then((response) => {
          if (response.ok) {
            resolve(response.blob());
          }
          reject(new Error('Network response was not ok.'));
        });
      }
    )},
    readUploadedFile(file) {
      const temporaryFileReader=new FileReader();

      return new Promise((resolve, reject) => {
        temporaryFileReader.onerror=() => {
          temporaryFileReader.abort();
          reject(new DOMException("Problem parsing input file."));
        };

        temporaryFileReader.onload=() => {
          resolve(temporaryFileReader.result);
        };
        temporaryFileReader.readAsArrayBuffer(file);
      });
    },
    async createAudioBuffer(arrayBuffer){
        var audioCtx = this.getAudioCtx;
        return new Promise((resolve, reject) => {
          audioCtx.decodeAudioData(arrayBuffer, resolve, reject);
        });
    },
    async createSample(sample){
      var blob = await this.fetchFile(sample.file);
      var arrayBuffer = await this.readUploadedFile(blob);
      var audioBuffer = await this.createAudioBuffer(arrayBuffer);
      this.$store.commit('addSamples', {sampleName:sample.name, buffer:audioBuffer});
      /*
      for (let i = 0; i < this.$store.state.samples.length; i++) {
        const sample = this.$store.state.samples[i];
        var audioBuffer = await this.createAudioBuffer(sample.src);
        sample.src = audioBuffer;
      }*/
    },
    initSequencer(){
      /*var sourceURL = require('@/assets/sounds/kick.wav');
      var blob = await this.fetchFile(sourceURL);
      var arrayBuffer = await this.readUploadedFile(blob);
      var audioBuffer = await this.createAudioBuffer(arrayBuffer);*/
      this.$store.commit('addDefaultSample',/*audioBuffer*/null);
      for (let i = 0; i < 3; i++) {
        this.$store.commit('addSamplesChosen',{sampleName:"Default", src:/*audioBuffer*/null});
      }
    },
  },
  async mounted(){
    /*var endUrl = (window.location.href.split('/').pop()); //On recupère la dernière valeur
    var preKit = endUrl.split('?');
    var kit = preKit[1].split("=");
    if(kit[0]==="initKit"){
      await fetch('https://banana-cobbler-95780.herokuapp.com/api/kit/'+this.id) //don't forget to change the url while dev/prod http://127.0.0.1:8000/api/kit/ or https://banana-cobbler-95780.herokuapp.com/api/kit/
      .then(response => response.json())
      .then(data => {
        console.log("oui");
          var data = JSON.parse(data.samples);
          var sampleList = [];
          data.forEach(sample => {
              sample.fields.file="https://vlmboiteason.s3.amazonaws.com/static/media/"+sample.fields.file;
              sampleList.push(sample.fields);
          });
          this.$store.commit('initKit',sampleList);
        });
        //this.waitKit;
    }*/
    this.$store.commit('createAudioCtx');
    this.initSequencer();
    if (this.$store.state.initWithKit) {
      for (let i = 0; i < this.$store.state.kitList.length; i++) {
        const sample = this.$store.state.kitList[i];
        this.createSample(sample);
      }
    }
    new Sortable(document.querySelectorAll('.channels-bodyWithoutButton'), {
      draggable: '.channel-draggable',
      handle: '.channel-control-label',
      mirror: {
        constrainDimensions: true,
      },
    });
  }
}
</script>

<style scoped>
.home{
  position: relative; 
  min-height: 100vh;
  width: 100%;
}
img{
   /* On met en place le fond d'écran */
  min-height: 100%;
  min-width: 1024px;
  /* On indique un redimensionnement proportionnel */
  width: 100%;
  height: auto;
  /* L'image est positionnée en haut à gauche */
  position: fixed;
  top: 0;
  left: 0;
  opacity:0.9;
}
.channels{
  padding: 0 4px 10px 4px;
  background-color: rgba(30, 30, 30, 0.9);
  min-width: 1030px;
  border: 2px solid rgb(96, 100, 105);
  border-radius: 0.5rem;
  position: relative;
  -webkit-box-align: center;
  align-items: center;
  box-sizing: border-box;
  transition: border-color 0.2s ease 0s;
  min-width: 1670px;
  scroll-snap-type: x mandatory;
}
.channels-body{
  max-height: 62vh;
  overflow-y: auto;

}
.channels-label{
    border: 2px solid rgb(96, 100, 105);
    color: rgb(144, 149, 153);
    background-color: rgb(32, 36, 39);
    font-weight: 600;
    font-size: 0.6rem;
    margin: 0px;
    padding: 0px 4px;
    position: absolute;
    left: 0.5rem;
    top: -0.6em;
    letter-spacing: 0.1em;
    border-radius: 3px;
    line-height: 1em;
    display: block;
    z-index: 1000;
}
.buttonAddChannel{
  font-size: 15px;
  width: 185px;
  height: 52px;
}
.btn-secondary:hover{
  background-color: #555 !important;
  border-color: #555;
}
.draggable-source--is-dragging {
  opacity: 0.2;
}

.draggable-mirror {
  opacity: 0.9;
  z-index: 10;
}
</style>
