<template>
    <div class="max-height" :id="'channel'+id">
        <div class="channel-control" :id="'channelControl'+id">
            <div class="channel-control-flex">
                <span class="channel-control-label" v-if="mySample.name == 'Default' ">CHANNEL {{mySample.id}}</span>
                <span class="channel-control-label" v-else>{{mySample.name}}</span>
                <div class="control-slot">
                    <ChannelFxTab :name="mySample.name" :id="mySample.id" :src="mySample.src" />
                </div>
                <div class="control-slot">
                    <SampleChooser :name="mySample.name" :id="mySample.id" :src="mySample.src"/>
                </div>
                <div class="timeline-slot">
                    <ChannelGrid :name="mySample.name" :id="mySample.id" :src="mySample.src"/>
                </div>
                <div class="control-slot" style="margin-left: -3px">
                    <div style="display: block">
                        <p style="padding:0; margin:0 5px; color: ghostwhite; font-weight: bold; font-size:1em">
                            Filter
                        </p>
                        <button style="background-color: transparent" class="buttonArrow" :id="'filterArrow'+id" @click="filterHide" >
                            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="black" class="bi bi-caret-down-fill" viewBox="0 0 16 16" >
                                <path d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"/>
                            </svg>
                    </button>
                    </div>
                    <ChannelConfig :name="mySample.name" :id="mySample.id" :src="mySample.src"/>
                </div>
                <div class="control-slot" style="display: flex;">
                    <button type="button" class="btn btn-primary" @click="resetGrid" style="border-top-right-radius: 0; border-bottom-right-radius: 0">
                        <svg version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" fill="#FFF"
                            width="24" height="24" viewBox="0 0 486.805 486.805" style="enable-background:new 0 0 486.805 486.805;"
                            xml:space="preserve">
                        <g>
                            <path d="M261.397,17.983c-88.909,0-167.372,51.302-203.909,129.073L32.072,94.282L0,109.73l52.783,109.565l109.565-52.786
                                l-15.451-32.066L89.82,161.934c30.833-65.308,96.818-108.353,171.577-108.353c104.668,0,189.818,85.154,189.818,189.821
                                s-85.15,189.824-189.818,189.824c-61.631,0-119.663-30.109-155.228-80.539l-29.096,20.521
                                c42.241,59.87,111.143,95.613,184.324,95.613c124.286,0,225.407-101.122,225.407-225.419S385.684,17.983,261.397,17.983z"/>
                        </g>
                        </svg>
                    </button>
                    <button v-if="$store.state.samplesChosen.length!==1" type="button" class="btn btn-danger" @click="deleteSample" style="border-top-left-radius: 0; border-bottom-left-radius: 0">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
                            <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                            <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                        </svg>
                    </button>
                </div>
            </div>
            <div class="filter d-none" :id="'filter'+id">
                <ChannelFilter :id="mySample.id" />
            </div>
        </div>
    </div>
</template>

<script>
import SampleChooser from '@/components/SampleChooser.vue'
import ChannelFxTab from '@/components/ChannelFxTab.vue'
import ChannelGrid from '@/components/ChannelGrid.vue'
import ChannelConfig from "@/components/ChannelConfig.vue";
import ChannelFilter from "@/components/ChannelFilter.vue";


export default {
    components: {
        SampleChooser,ChannelFxTab, ChannelGrid, ChannelConfig, ChannelFilter
    },
    data(){
        return{
            filter: false,
        }
    },
    props:['name','id','src'],
    computed:{
        mySample(){
            const chosenSample = this.$store.state.samplesChosen.find(sample => sample.id===this.id);
            return chosenSample;
        },
        nbBeats(){
            return this.$store.state.nbBeats;
        },
        documentWidth(){
            return document.documentElement.clientWidth;
        }
    },
    methods:{
        resizeDiv(){
            if(this.mySample !== undefined){
                document.getElementById('channel'+this.mySample.id).style.width = 35.8 + this.nbBeats*(1/16)*((16/100)*document.documentElement.clientWidth) + (this.nbBeats)*(1/16)*((0.5/100)*document.documentElement.clientWidth) +'rem';
            }
            if(document.documentElement.clientWidth<1670){
                document.getElementById("channel"+this.mySample.id).style.width = ((271+8)*this.nbBeats+580)+"px";
            }
        },
        filterHide(){
            var idButton = "filterArrow" + this.id
            document.getElementById(idButton).disabled = true;
            var idChannel = "channel" + this.id
            var idChannelControl = "channelControl" + this.id
            var idFilter= "filter" + this.id
            if(this.filter){
                document.getElementById(idButton).classList.remove("activeArrow");
                window.setTimeout(()=>{
                    document.getElementById(idFilter).classList.add("d-none");
                    document.getElementById(idChannel).style.overflowY = "visible";
                }, 500);
                document.getElementById(idChannel).style.maxHeight = "110px";
                document.getElementById(idChannel).style.overflowY = "hidden";
                document.getElementById(idChannelControl).style.maxHeight = "90px";
                this.filter= false;
            }
            else{
                document.getElementById(idButton).classList.add("activeArrow");
                document.getElementById(idFilter).classList.remove("d-none");
                document.getElementById(idChannel).style.maxHeight = "550px";
                document.getElementById(idChannel).style.overflowY = "hidden";
                document.getElementById(idChannelControl).style.maxHeight = "530px";
                this.filter = true;
            }
            setTimeout(()=>{
                document.getElementById(idButton).disabled = false;
            }, 500)
        },
         deleteSample(){
            this.$store.commit('deleteSamplesChosen',this.mySample.id);
        },
        resetGrid(){
            for (let i = 0; i < this.mySample.timeSubdiv*this.nbBeats; i++) {
                var id=i+1;
                var sample = ('temps-ref-'+this.mySample.id.toString()+'-'+id.toString());
                var div = document.getElementById(sample);
                div.classList.remove('active3');
                div.classList.remove('active2');
                div.classList.remove('active1');
                this.$store.commit('setNote', {sampleId: this.mySample.id, noteId:id, gainNote: 0});

                var backgroundId = 'background-'+(id);
                var background = document.getElementById(backgroundId);;
                background.style.top = "40px";
                background.style.transform= `translateY(0px)`;
                background.style.height= 0 + "px";
                var pitch = "pitch-" + (id);
                var dragItem = document.getElementById(pitch);
                dragItem.style.transform = "translate3d(" + 0 + "px, " + 30 + "px, 0)";
                this.$store.commit("resetChannel", {sampleId: this.mySample.id, newVal: true});
            }
        }
    },
    mounted(){
        window.addEventListener("resize", this.resizeDiv);
        if(document.documentElement.clientWidth<1670){
            document.getElementById("channel"+this.mySample.id).style.width = ((271+8)*this.nbBeats+580)+"px";
        }
        else{
            document.getElementById("channel"+this.mySample.id).style.width = 35.8 + this.nbBeats*(1/16)*((16/100)*document.documentElement.clientWidth) + (this.nbBeats)*(1/16)*((0.5/100)*document.documentElement.clientWidth) +'rem';
        }
    },
    watch:{
        nbBeats(newVal){
            if(this.mySample !== undefined){
                if(document.documentElement.clientWidth<1670){
                    document.getElementById("channel"+this.mySample.id).style.width = ((271+8)*newVal+580)+"px";
                }
                else{
                    document.getElementById("channel"+this.mySample.id).style.width = 35.8 + newVal*(1/16)*((16/100)*document.documentElement.clientWidth) + (newVal)*(1/16)*((0.5/100)*document.documentElement.clientWidth) +'rem';
                }
            }
        }
    }
}

</script>

<style scoped>
.max-height{
    max-height: 110px;
    transition: max-height 0.5s;
    overflow-y: visible;
}
.channel-control{
    max-height: 90px;
    margin: 12px 4px ;
    padding: 3px;
    border: 2px solid rgb(96, 100, 105);
    border-radius: 0.5rem;
    box-sizing: border-box;
    transition: border-color 0.2s ease 0s;
    transition: max-height 0.5s;
}
.channel-control-flex{
    display: flex;
    position: relative;
    -webkit-box-align: center;
    align-items: center;
}
.channel-control-label{
    color: rgb(144, 149, 153);
    background-color: rgb(32, 36, 39);
    font-weight: 600;
    font-size: 0.6rem;
    margin: 0px;
    padding: 0px 4px;
    position: absolute;
    left: 0.5rem;
    top: -0.9em;
    letter-spacing: 0.1em;
    border-radius: 3px;
    line-height: 1em;
    display: block;
    text-transform: uppercase;
    cursor: move;
}
.control-slot{
    box-sizing: border-box;
    display: flex;
    align-items: center;
    margin: 0.4rem 0.25rem;
    padding: 0.3rem;
    background-color: rgb(136, 136, 136);
    border-radius: 6px;
    height: 4rem;
}
.timeline-slot{
    box-sizing: border-box;
    display: flex;
    align-items: center;
    height: 4rem;
}

.buttonArrow {
   transition: all 0.5s;
   border: none;
}
.activeArrow{
	-webkit-transform: rotate(180deg);
	-moz-transform: rotate(180deg);
	transform: rotate(180deg);
} 
.filter{
    transition: all 0.5s;
}
</style>