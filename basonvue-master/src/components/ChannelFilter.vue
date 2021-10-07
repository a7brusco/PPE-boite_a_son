<template>
    <div style="display: flex;">
    <div style="height: 450px; margin-top: 1rem;" :id="'divCanvas'+mySample.id">
        <div class="selector-container">
            <CustomSelect
            :options="allFilters"
            :default="mySample.filterName"
            :numberOfLetters="8"
            @input="setFilter($event)"
            class="selector"
            />
        </div>
        <div style="display:block; margin-top: 15px">
            <canvas :id="'freqResponse'+mySample.id" width="200" height="300"></canvas>
        </div>
    </div>
        <div class="control-slot" style="margin: 1rem 0 0 0.3rem;" :id="'controlSlotFilter'+mySample.id">
            <div style="display: flex">
                <div class="knob-slot frequencySlider" >
                    <span class="knob-name" style="margin-left: 65px; margin-bottom: 8px;">Freq</span>
                    <div style="display: flex">
                        <div style="height: 300px; font-size; color: ghostwhite; margin: 0 0.25rem 0 0.5rem;">   
                            <p style="margin: -9px 2px 0 1px;">20kHz -</p>
                            <p style="margin: 5px 2px 0 1px">10kHz -</p>
                            <p style="margin: 4px 2px 0 10px">5kHz -</p>
                            <p style="margin: 16px 2px 0 10px">2kHz -</p>
                            <p style="margin: 6px 2px 0 10px">1kHz -</p>
                            <p style="margin: 3px 2px 0 1px">500Hz -</p>
                            <p style="margin: 16px 2px 0 1px">200Hz -</p>
                            <p style="margin: 6px 2px 0 1px">100Hz -</p>
                            <p style="margin: 5px 2px 0 10px">50Hz -</p>
                            <p style="margin: 15px 2px 0 10px">20Hz -</p>
                        </div>
                        <div class="knob">
                            <webaudio-slider
                                :src="freqKnobData.imageURL"
                                :knobsrc="freqKnobData.imageButtonUrl"
                                :min="freqKnobData.min"
                                :max="freqKnobData.max"
                                :width="freqKnobData.width"
                                :height="freqKnobData.height"
                                :step="freqKnobData.step"
                                :id="'freq'+id"
                                :valuetip="1"
                                conv="(Math.pow(10,x)*20).toFixed(0)"
                                direction="vert"
                                @input="setFrequencyFilter">
                            </webaudio-slider>
                        </div>
                    </div>
                </div>
                <div style="display: flex; margin: 1.4rem 0 0 1.1rem;">
                    <div style="background-color: black; height: 300px; display:flex;" :style="{width: 16*$store.state.nbBeats+(($store.state.nbBeats-1)*8*100/documentWidth)- 0.9 +'vw', minWidth: 271*$store.state.nbBeats + (($store.state.nbBeats-1)*8) - 8 + 'px'}" id="containerAutomation">
                        <PointAutomation v-for="n in ($store.state.nbBeats*14)" :key="n"  :id="mySample.id" :idPoint="n" :x="n" :y="(3-Math.log10(mySample.frequencyInTime[n-1]/20))*98.33" :freqInitial="frequency" :color="filterColor"/>
                    </div>
                </div>
            </div>
            <div class="separation">
            </div>
            <div class="knob-slot" style="margin-left:27px">
                <span class="knob-name">Q</span>
                <div class="knob">
                    <span class="knob-label">0.01</span>
                    <webaudio-knob
                        :src="QKnobData.imageURL"
                        :knobsrc="QKnobData.imageButtonUrl"
                        :min="QKnobData.min"
                        :max="QKnobData.max"
                        :width="QKnobData.size"
                        :height="QKnobData.size"
                        :step="QKnobData.step"
                        :id="'Q'+id"
                        :value="1"
                        :valuetip="1"
                        @dblclick="setQFilter(true)"
                        @input="setQFilter(false)">
                    </webaudio-knob>
                    <span class="knob-label">10.00</span>
                </div> 
            </div>
        </div>
        
    </div>
</template>

<script>
import {
  Chart,
  ArcElement,
  LineElement,
  BarElement,
  PointElement,
  BarController,
  BubbleController,
  DoughnutController,
  LineController,
  PieController,
  PolarAreaController,
  RadarController,
  ScatterController,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  RadialLinearScale,
  TimeScale,
  TimeSeriesScale,
  Decimation,
  Filler,
  Legend,
  Title,
  Tooltip
} from 'chart.js';

Chart.register(
  ArcElement,
  LineElement,
  BarElement,
  PointElement,
  BarController,
  BubbleController,
  DoughnutController,
  LineController,
  PieController,
  PolarAreaController,
  RadarController,
  ScatterController,
  CategoryScale,
  LinearScale,
  LogarithmicScale,
  RadialLinearScale,
  TimeScale,
  TimeSeriesScale,
  Decimation,
  Filler,
  Legend,
  Title,
  Tooltip
);
import '@/assets/js/webaudio-controls.js'
import freqKnobImage from '@/assets/images/knobs/roland_SH_101_knob.png'
import buttonSLiderImage from '@/assets/images/knobs/Kop.png'
import QKnobImage from '@/assets/images/knobs/maschine-default.png'
import PointAutomation from '@/components/PointAutomation.vue'
import CustomSelect from "@/components/CustomSelect.vue";

export default ({
    components: {
        PointAutomation, CustomSelect
    },
    data(){
        return{
            frequency: 20,
            Q: 1,
            freqKnobData: {imageURL:freqKnobImage, imageButtonUrl: buttonSLiderImage, min:0, max:3, step:0.0001, width:20, height: 300},
            QKnobData: {imageURL:QKnobImage, min:0.01, max:10, step:0.01, size: 40},
            canvasData: {height:300, range:500},
            cercle: [],
            recCanvas:null,
            allFilters: ["Bypass", "Lowpass","Highpass", "Bandpass"],
            chart: null,
            chartIsDrawing: false,
            oldFreq: 20,
            oldFilter: 'Bypass',
            oldQ: 1
        };
    },
    props:['id'],
    computed:{
        mySample(){
            const chosenSample = this.$store.state.samplesChosen.find(sample => sample.id===this.id);
            return chosenSample;
        },
        frequencyChange(){
            if(this.mySample !== undefined){
                return this.mySample.fxParams.frequency;
            }
        },
        isPlaying(){
            return this.$store.state.isPlaying;
        },
        documentWidth(){
            return document.documentElement.clientWidth;
        },
    },
    methods:{
        drawFrequencyResponse(){
            if((this.oldFreq!==this.mySample.audioNode.filter.frequency.value || this.oldFilter!==this.mySample.filterName || this.oldQ!==this.mySample.audioNode.filter.Q.value) && !this.$store.state.isPlaying){
                
                this.oldFreq = this.mySample.audioNode.filter.frequency.value;
                this.oldFilter = this.mySample.filterName;
                this.oldQ = this.mySample.audioNode.filter.Q.value;
                var canvas = document.getElementById('freqResponse'+this.mySample.id);
                if(this.chart!==null){
                    this.chart.destroy();
                }
                var myFrequencyArray = new Float32Array(400);
                var magResponseOutput = new Float32Array(400);
                var phaseResponseOutput = new Float32Array(400);
                for(var i=0; i<myFrequencyArray.length; i++){
                    if(i<10){
                        myFrequencyArray[i] = 20 + i*2;
                    }
                    else if(i<50){
                        myFrequencyArray[i] = 20 + 10*2 + (i-10)*5;
                    }
                    else if(i<100){
                        myFrequencyArray[i] = 20 + 10*2 + 50*5 + (i-60)*10;
                    }
                    else if(i<150){
                        myFrequencyArray[i] = 20 + 10*2 + 50*5 + 50*10 + (i-110)*20;
                    }
                    else if(i<200){
                        myFrequencyArray[i] = 20 + 10*2 + 50*5 + 50*10 + 50*20 + (i-160)*40;
                    }
                    else{
                        myFrequencyArray[i] = 20 + 10*2 + 50*5 + 50*10 + 50*20 + 50*40 + (i-210)*83,4211; //To obtain 20000 at the end
                    }
                }
                this.mySample.audioNode.filter.getFrequencyResponse(myFrequencyArray, magResponseOutput,phaseResponseOutput); //Changert que si la fr"quence à changée ou le filtre
                for(var i=0; i<magResponseOutput.length; i++){
                    magResponseOutput[i] = 20*Math.log(magResponseOutput[i]);
                } 
                const data = {
                    labels: myFrequencyArray,
                    datasets: [{
                        label: 'Filtre',
                        backgroundColor: this.mySample.filterColor,
                        borderColor: this.mySample.filterColor,
                        data: magResponseOutput,
                        pointRadius: 1,
                    },
                    {   
                        label: "0dB",
                        backgroundColor: 'rgb(255, 255, 255)',
                        borderColor: 'rgb(255, 255, 255)',
                        data: new Float32Array(400),
                        pointRadius: 1,
                    },
                    ]

                };
                this.chart = new Chart(canvas.getContext("2d"), {
                    type: "line",
                    data: data,
                    options:{
                        plugins: {
                            title: {
                                display: true,
                                text: 'Réponse fréquentielle',
                                padding: {
                                    bottom: 30
                                }
                            },
                            legend: {
                                display: false
                            },
                        },
                        
                        scales: {
                            y:{
                                max: 20,
                                min: -100,
                                title:{
                                    display: true,
                                    text:"dB",
                                    padding: 2
                                }
                            },
                            x: {
                                type: 'logarithmic',
                                min: 20,
                                max: 20000,
                                title:{
                                    display: true,
                                    text:"Hz",
                                }
                            },
                        }
                    }
                });
                canvas.style.width = "200px";
                canvas.style.height= "300px";
            }
            this.chartIsDrawing= false;
        },
        setFilter(event){
            var sample = this.mySample;
            if(event==="Bypass"){
                sample.filterColor = "#333333";
                sample.audioNode.filter.type = "allpass";
            }
            else if(event==="Lowpass"){
                sample.filterColor = "red";
                sample.audioNode.filter.type = event.toLowerCase();
            }
            else if(event==="Highpass"){
                sample.filterColor = "green";
                sample.audioNode.filter.type = event.toLowerCase();
            }
            else{
                sample.filterColor = "blue";
                sample.audioNode.filter.type = event.toLowerCase();
            }
            sample.filterName = event;
            var freq = parseFloat(document.getElementById("freq" + sample.id).value);
            freq = (Math.pow(10,freq)*20).toFixed(0);
            sample.audioNode.filter.frequency.setValueAtTime(freq, this.$store.state.audioCtx.currentTime);
            sample.audioNode.filter.Q.setValueAtTime(parseFloat(document.getElementById("Q" + sample.id).value), this.$store.state.audioCtx.currentTime);
            if(!this.chartIsDrawing){
                this.chartIsDrawing = true;
                setTimeout(this.drawFrequencyResponse, 1200);
            }
        },
        setFrequencyFilter(){
            if(this.mySample.sliderFreqDisabled){
                var sample = this.mySample;
                sample.audioNode.filter.frequency.value = sample.fxParams.frequency;
                var idSliderFreq = 'freq' + this.id
                var sliderFreq = document.getElementById(idSliderFreq);
                sliderFreq.setValue(Math.log10(sample.fxParams.frequency/20));
            }
            else{
                var sample = this.mySample;
                var freq = parseFloat(document.getElementById("freq" + sample.id).value);
                freq = (Math.pow(10,freq)*20).toFixed(0);
                sample.audioNode.filter.frequency.setValueAtTime(freq, this.$store.state.audioCtx.currentTime);
                sample.fxParams.frequency = freq;
                this.frequency = freq;
            }
            if(!this.chartIsDrawing){
                this.chartIsDrawing = true;
                setTimeout(this.drawFrequencyResponse, 1200);
            }
        },
        setQFilter(reset){
            var sample = this.mySample;
            if(!reset){
                sample.audioNode.filter.Q.setValueAtTime(parseFloat(document.getElementById("Q" + sample.id).value), this.$store.state.audioCtx.currentTime);
                this.Q = parseFloat(document.getElementById("Q" + sample.id).value);
            }
            else{
                sample.audioNode.filter.Q.setValueAtTime(1, this.$store.state.audioCtx.currentTime);
                this.Q = 1;
                var QKnob = document.getElementById("Q"+sample.id);
                QKnob.setValue(1);
            }
            if(!this.chartIsDrawing){
                this.chartIsDrawing = true;
                setTimeout(this.drawFrequencyResponse, 1200);
            }
            
        },
        resizeAutomation(){
            if(document.documentElement.clientWidth >= 1670){
                document.getElementById("containerAutomation").style.width = 16*this.$store.state.nbBeats + ((this.$store.state.nbBeats-1)*8*100/document.documentElement.clientWidth) - 0.9 + 'vw';
            }
            else{
                 document.getElementById("containerAutomation").style.width = 271*this.$store.state.nbBeats + ((this.$store.state.nbBeats-1)*8) - 8 + "px";
            }
        }
    },
    watch: {
        frequencyChange(newVal, oldVal){
            if(this.mySample !== undefined){
                var sample = this.mySample;
                sample.audioNode.filter.frequency.value = newVal;
                var idSliderFreq = 'freq' + this.id
                var sliderFreq = document.getElementById(idSliderFreq);
                sliderFreq.value = Math.log10(newVal/20);
            }
        },
        isPlaying(newVal){
            if(newVal){
                document.getElementById("freq"+this.mySample.id).style.opacity = '0.5';
                
            }
            else{
                document.getElementById("freq"+this.mySample.id).style.opacity = '1';
            }
        },
    },
    mounted(){
        this.drawFrequencyResponse();
        window.addEventListener("resize", this.resizeAutomation);
    }
})
</script>

<style scoped>
.control-slot{
    box-sizing: border-box;
    justify-items: middle;
    margin: 0.5rem;
    padding: 0.5rem;
    background-color: rgb(136, 136, 136);
    border-radius: 6px;
    width: auto;
    height: 410px;
}
.knob-slot{
    box-sizing: border-box;
}
.knob-name{
    padding: 0;
    margin: 4px 0 0 37px;
    font-weight: bold;
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
.frequencySlider{
    margin: auto -0.75rem;
}   
.separation{
    border-bottom: 3px solid #313131;
    margin: 10px 0
}
.canvasWrapperDraw{
    margin: 2rem auto auto 18rem;
    height: 300px;
}
.canvasDraw{
    height: 300px;
}
.dropdown-toggle::after {
    margin-left: 0;
    content: "";
    border-top: .3em solid;
    border-right: .3em solid transparent;
    border-bottom: 0;
    border-left: .3em solid transparent;
    float: right;
    margin-top: 0.5em;
}

.btn-dark{
 background-color: #0a0a0a;
 border-radius: 10px;
}
.dark{
    background-color: #0a0a0a;
    color: ghostwhite;
}
.itemSelected{
    background-color: #222222;
}
.itemSelect{
    cursor: pointer;
}
.dropdown-menu{
    padding: 0;
}

.dropdown-menu li a:hover{
    background-color: #222222;
    color:ghostwhite;
}
.selector-container{
    box-sizing: border-box;
    width: 8rem;
    height: 3rem;
    display: flex;
    margin-left:0.5rem;
    align-items: center;
    justify-content: center;
}
</style>