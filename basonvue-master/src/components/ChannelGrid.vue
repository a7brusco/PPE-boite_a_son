<template>
    <div v-for="i in nbBeats" :key="i" style="display: inline-block; height: 4rem; margin-right: 8px; width: 16vw" :class="{start_mesure: i==1}" class="min-width-beat"> 
        <Note v-for="n in mySample.timeSubdiv" :key="n+mySample.timeSubdiv*(i-1)" :indexNbSub="n" :indexNbTemps="i" :idSample="mySample.id"/>
    </div>
</template>

<script>
import Note from '@/components/Note.vue'

export default ({
    components: {
        Note
    },
    props: ['id', 'name', 'src'],
    computed: {
        mySample(){
            const chosenSample = this.$store.state.samplesChosen.find(sample => sample.id===this.id);
            return chosenSample;
        },
        nbBeats(){
            return this.$store.state.nbBeats;
        },
    },
})
</script>

<style scoped>
.btn:active, .btn:focus{
    box-shadow: none;
}
.centerDiv{
    box-sizing: border-box;
}
.sampleControl{
    position: absolute;
    top: 11rem;
    margin: 16px;
}
.active1{
    background-color: red !important;
}

.active2{
    background-color: orange !important;
}

.active3{
    background-color: greenyellow !important;
}

.border_bottom{
    border-bottom: 0.1rem solid white
}

.margin_left{
    margin-left: 1rem;
}

.start_mesure{
    margin-left: 0.5rem;
}
.hidden{
    display: none;
}
.min-width-beat{
    min-width: 271px;
}
</style>>

