<template>
    <div class="selector-container">
            <CustomSelect
            :options="allNbSubdivisions"
            :default="mySample.timeSubdiv.toString()"
            :id="'nbSubDiv'+mySample.id"
            @input="setNbSubdivisions($event)"
            class="selector"
            />
    </div>
    
    
</template>

<script>
import CustomSelect from "@/components/CustomSelect.vue";

export default {
    components: {
        CustomSelect
    },
    data(){
        return{
            allNbSubdivisions: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']
        }
    },
    computed:{
        mySample(){
            const chosenSample = this.$store.state.samplesChosen.find(sample => sample.id===this.id);
            return chosenSample;
        },
        nbBeats(){
            return this.$store.state.nbBeats;
        },
    },
    methods:{
        setNbSubdivisions(e){
            var divsActivate = document.getElementsByName("noteOf"+this.mySample.name+this.mySample.id);
            for(var i=0; i<divsActivate.length; i++){
                divsActivate[i].classList.remove("active1");
                divsActivate[i].classList.remove("active2");
                divsActivate[i].classList.remove("active3");
            }
            this.$store.commit("changeTrack", {sampleId: this.mySample.id, newSubDiv: parseInt(e)});                          
        },
    },
    props:['name','id','src'],
}
</script>

<style scoped>
.selector-container{
    box-sizing: border-box;
    width: 4rem;
    height: 2rem;
    display: flex;
    margin: 0 0.25rem 0 0.25rem;
    align-items: center;
    justify-content: center;
}
.custom-select{
    height:  2rem;
    line-height: 2em;
}
</style>