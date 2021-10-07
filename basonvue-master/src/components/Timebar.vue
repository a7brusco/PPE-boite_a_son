<template>
    <div style="display: grid; align-items: start; position: relative; height:30px" :style="{gridTemplateColumns: 26.25 +'rem '+ 22*nbBeats +'rem ' + 'auto', width: nbBeats*16.5 + 1 + 'vw'}">
        <div class="divProgress" :style="{width: nbBeats*16.5 + 'vw', minWidth: nbBeats*(271 + 8) + 'px'}" id="barProgress">
            <div class="progress" id="progress">
                <p v-for="i in nbBeats" :key="i" :id="'indicator'+i" class="numberOfMesure" :style="[i===1 ? {'margin-left': 0.25 + 'vw'} : {'margin-left': Math.max(16.42*(documentWidth/100)*(i-1)-0.25*(documentWidth/100),(271+8)*(i-1))+'px'}]">{{i}}</p>
            </div>
        </div> 
    </div>
</template>

<script>
export default {
    computed:{
        nbBeats(){
            return this.$store.state.nbBeats;
        },
        documentWidth(){
            return document.documentElement.clientWidth;
        }
    },
    methods:{
        resizeIndicator(){
            for(var i = 1; i<this.$store.state.nbBeats; i++){
                document.getElementById("indicator"+(i+1)).style.marginLeft = Math.max(16.42*(document.documentElement.clientWidth/100)*(i)-0.25*(document.documentElement.clientWidth/100),(271+8)*(i))+'px';
            }
        },
    },
    mounted(){
        window.addEventListener("resize", this.resizeIndicator);
    }
}
</script>

<style scoped>
.progress {
  width: 0%;
  height: 22px;
  background: rgba(0, 0, 0, 0) linear-gradient(190deg ,#111, #333) repeat scroll 0% 0%;
  transition: border-color 0.2s ease 0s;
  transition: width linear;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}

.numberOfMesure{
  position: absolute; 
  font-weight: bold; 
  color: ghostwhite; 
  font-size: 1rem;
}
.divProgress{
  margin: 0 1rem 0rem 18.5rem; 
  height: 24px;
  border: 2px solid rgb(96, 100, 105); 
  border-top-width: 0;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  background-color: rgba(60,60,60, 0.5);
}
</style>