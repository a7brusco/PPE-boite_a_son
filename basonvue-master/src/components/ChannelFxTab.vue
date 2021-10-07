<template>
    <div class="knob-slot" style="margin-right: 10px;">
        <span class="knob-name">VOL</span>
        <div class="knob">
            <span class="knob-label">0</span>
            <webaudio-knob
                :src="volKnobData.imageURL"
                :min="volKnobData.min"
                :max="volKnobData.max"
                :width="volKnobData.size"
                :height="volKnobData.size"
                :value="100"
                :id="'volume'+mySample.id"
                @input="updateGain"
                @dblclick="resetGain"
                :valuetip="1">
            </webaudio-knob>
            <span class="knob-label">1</span>
        </div>
    </div>
    <div class="knob-slot">
        <span class="knob-name">PAN</span>
        <div class="knob">
            <span class="knob-label">L</span>
            <webaudio-knob
                :src="panKnobData.imageURL"
                :min="panKnobData.min"
                :max="panKnobData.max"
                :width="panKnobData.size"
                :height="panKnobData.size"
                :id="'pan'+mySample.id"
                @input="updatePan"
                @dblclick="resetPan"
                :valuetip="1">
            </webaudio-knob>
            <span class="knob-label">R</span>
        </div>
    </div>
</template>

<script>
import '@/assets/js/webaudio-controls.js'
import volKnobImage from '@/assets/images/knobs/maschine-default.png'
import panKnobImage from '@/assets/images/knobs/maschine-bipolar.png'

export default {
    data(){
        return {
            volKnobData: {imageURL:volKnobImage, min:0, max:100, size:40},
            panKnobData: {imageURL:panKnobImage, min:-100, max:100, size:40},
        };
    },
    props:["id", "name", "src"],
    computed:{
        mySample(){
            const chosenSample = this.$store.state.samplesChosen.find(sample => sample.id===this.id);
            return chosenSample;
        },
        getAudioCtx(){
            return this.$store.getters.getAudioCtx;
        },
    },
    methods:{
        updateGain(){
            var id = 'volume'+this.mySample.id;
            var value = (document.getElementById(id).value/100);
            this.$store.commit('updateGain',{value: value , sampleId: this.mySample.id});
        },
        updatePan(){
            var id = 'pan'+this.mySample.id;
            var value = (document.getElementById(id).value/100);
            this.$store.commit('updatePan',{value: value , sampleId: this.mySample.id});
            
        },
        resetPan(){
            var id = 'pan'+this.mySample.id;
            document.getElementById(id).setValue(0);
            this.$store.commit('updatePan',{value: 0, sampleId: this.mySample.id});
        },
        resetGain(){
            var id = 'volume'+this.mySample.id;
            document.getElementById(id).value = 100;
            document.getElementById(id).shadowRoot.children[1].children[0].textContent = 100;
            this.$store.commit('updateGain',{value: 1 , sampleId: this.mySample.id});
        }
    }
}
</script>

<style scoped>
.knob-slot{
    box-sizing: border-box;
}
.knob-name{
    padding: 0;
    margin: 0 0 4px;
    font-weight: bold;
    text-align: center;
    font-size: 0.7rem;
    line-height: 1em;
    color: ghostwhite;
    display: block;
    text-transform: uppercase;
}
.knob{
    display: flex;
    align-items: baseline;
    -webkit-box-align: baseline;
    box-sizing: border-box;
}
.knob-label{
    margin: 0;
    padding: 0;
    opacity: 0.7;
    line-height: 1em;
    display: block;
    font-size: 0.7em;
    text-transform: uppercase;
    color: ghostwhite;
}
</style>