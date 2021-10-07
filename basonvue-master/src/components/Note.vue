<template>
    <div :ref="'temps-ref-'+(indexNbSub+mySample.timeSubdiv*(indexNbTemps-1))" :id="'temps-ref-'+mySample.id.toString()+'-'+(indexNbSub+mySample.timeSubdiv*(indexNbTemps-1))" :name="'noteOf'+mySample.name+mySample.id" style="background-color: #888888; height: 4rem; display: inline-block; border-radius: 5px; margin-right: 8px" :style="{width: (15.5/mySample.timeSubdiv - (8*(100/documentWidth))) + 'vw', minWidth: ((271-8*mySample.timeSubdiv)/mySample.timeSubdiv) + 'px'}" @click.exact="active(indexNbSub+mySample.timeSubdiv*(indexNbTemps-1))" @click.ctrl="reset(indexNbSub+mySample.timeSubdiv*(indexNbTemps-1))">
        <div id="container" :ref="'container-'+(indexNbSub+mySample.timeSubdiv*(indexNbTemps-1))" style="height: inherit; width: inherit"
        @mousedown="dragStart" 
        @mouseup="dragEnd" 
        @mousemove="drag"
        @mouseout="makeMouseOutFn">
            <div  :ref="'background-'+(indexNbSub+mySample.timeSubdiv*(indexNbTemps-1))" :id="'background-'+(indexNbSub+mySample.timeSubdiv*(indexNbTemps-1))" style="height: 0px; position: absolute; background-color: #222; opacity: 0.2" :style="{width:  (15.5/mySample.timeSubdiv - (8*(100/documentWidth))) + 'vw', minWidth: ((271-8*mySample.timeSubdiv-4)/mySample.timeSubdiv) + 'px'}">
            </div>
            <div class="item" :ref="'pitch-'+(indexNbSub+mySample.timeSubdiv*(indexNbTemps-1))" :id="'pitch-'+(indexNbSub+mySample.timeSubdiv*(indexNbTemps-1))" :style="{minWidth: ((271-8*mySample.timeSubdiv)/mySample.timeSubdiv) + 'px'}">
            </div>
        </div>
    </div>
</template>

<script>
export default ({
    data(){
        return{
            activeDrag: false,
            currentY: 30,
            initialY: 30,
            yOffset: 30,    
            pitch: false,
        }
    },
    props: ['indexNbSub', 'indexNbTemps', 'idSample'],
    computed:{
        mySample(){
            const chosenSample = this.$store.state.samplesChosen.find(sample => sample.id===this.idSample);
            return chosenSample;
        },
        resetChannel(){
            if(this.mySample!==undefined){
                return this.mySample.resetChannel;
            }
        },
        documentWidth(){
            return document.documentElement.clientWidth;
         },
    },
    methods:{
         reset(id){
            var sample = ("temps-ref-" + id);
            var div = this.$refs[sample];
            div.classList.remove('active3');
            div.classList.remove('active2');
            div.classList.remove('active1');
            this.$store.commit('setNote', {sampleId: this.idSample, noteId:id, gainNote: 0});
         },
         active(id){
            if(!this.pitch){
                var sample = ("temps-ref-" + id);
                var div = this.$refs[sample];
                if(div.classList.contains("active3")){
                    div.classList.remove("active3");
                    this.$store.commit('setNote', {sampleId: this.idSample, noteId:id, gainNote: 0});
                }
                else{
                    if(div.classList.contains("active1")){
                        div.classList.remove("active1");
                        div.classList.add("active2");
                        this.$store.commit('initAudio',this.idSample);
                        this.$store.commit('setNote', {sampleId: this.idSample, noteId:id, gainNote: 0.5});
                        if(!this.$store.state.isPlaying){
                            this.$store.commit('playNote', {sampleId: this.idSample, gainNote: 0.5, pitchNote: this.mySample.track[id-1]["pitch"]});
                        }
                    }
                    else if(div.classList.contains("active2")){
                        div.classList.remove("active2");
                        div.classList.add("active3");
                        this.$store.commit('initAudio',this.idSample);
                        this.$store.commit('setNote', {sampleId: this.idSample, noteId:id, gainNote: 0.25});
                        if(!this.$store.state.isPlaying){
                            this.$store.commit('playNote', {sampleId: this.idSample, gainNote: 0.25, pitchNote: this.mySample.track[id-1]["pitch"]});
                        }
                    }
                    else{
                        div.classList.add("active1");
                        this.$store.commit('initAudio',this.idSample);
                        this.$store.commit('setNote', {sampleId: this.idSample, noteId:id, gainNote: 1});
                        if(!this.$store.state.isPlaying){
                            this.$store.commit('playNote', {sampleId: this.idSample, gainNote: 1,pitchNote: this.mySample.track[id-1]["pitch"]});
                        }
                    }
                }
            }
            this.pitch = false;
        },
        dragStart(e){
            var pitch = ("pitch-" + (this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1)));
            var dragItem = this.$refs[pitch];
            if (e.type === "touchstart") {
                this.initialY = e.touches[0].clientY - this.yOffset;
            } else {
                this.initialY = e.clientY - this.yOffset;
            }

            if (e.target === dragItem) {
                var noteId = ("temps-ref-" + (this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1)));
                var note = this.$refs[noteId];
                note.style.cursor = "ns-resize";
                this.activeDrag = true;
                this.pitch = true
            }
        },
        dragEnd(e) {
            var noteId = ("temps-ref-" + (this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1)));
            var note = this.$refs[noteId];
            note.style.cursor = "initial";
            this.initialY = this.currentY;
            if(this.activeDrag){
                this.$store.commit("setPitchNote", {valuePitch: this.currentY, max: 60, noteId: this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1), sampleId: this.idSample});
            }
            this.activeDrag = false;
        },
        drag(e) {
            if (this.activeDrag){
                var backgroundId = 'background-'+(this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1));
                var background = this.$refs[backgroundId];
                var pitch = ("pitch-" + (this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1)));
                var dragItem = this.$refs[pitch];
                e.preventDefault();
                if (e.type === "touchmove") {
                    this.currentY = e.touches[0].clientY - this.initialY;
                } 
                else { 
                    if((e.clientY - this.initialY)<=60 && (e.clientY - this.initialY)>=0){
                        this.currentY = e.clientY - this.initialY;
                    }
                }
                if(this.currentY<=34 && this.currentY>=24)
                {
                    this.yOffset = this.currentY;
                    this.currentY = 30;
                    background.style.height= "0px";
                    this.setTranslate(this.currentY, dragItem);
                }
                else{
                    this.yOffset = this.currentY;
                    if(this.currentY - 30 > 0){
                        background.style.top = "40px";
                        background.style.transform= `translateY(0px)`;
                        background.style.height= Math.abs(this.currentY-30) + "px";
                    }
                    else{
                        background.style.top = "40px";
                        background.style.transform= `translateY(${-Math.abs(this.currentY-30)}px)`;
                        background.style.height= Math.abs(this.currentY-30) + "px";
                    }
                    this.setTranslate(this.currentY, dragItem);
                }
            }
        },
        setTranslate(yPos, el) {
            el.style.transform = "translate3d(" + 0 + "px, " + yPos + "px, 0)";
        },
        makeMouseOutFn(e){
            var containerId = 'container-'+(this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1));
            var container = this.$refs[containerId];
            var list = this.traverseChildren(container);
            var event = e.toElement || e.relatedTarget;
            if (!!~list.indexOf(event)) {
                return;
            }
            if(this.activeDrag){
                this.active(0);
            }
            this.dragEnd();
        },   
        traverseChildren(elem){
            var children = [];
            var q = [];
            q.push(elem);
            while (q.length > 0) {
            var elem = q.pop();
            if(elem !== undefined){
                children.push(elem);
                pushAll(elem.children);
                }
                function pushAll(elemArray){
                for(var i=0; i < elemArray.length; i++) {
                    q.push(elemArray[i]);
                }
                }
            }
            return children;
        },
        resizeNote(){
            if(document.documentElement.clientWidth>1650 && this.mySample!==undefined){
                var noteId = 'temps-ref-'+this.mySample.id.toString()+'-'+(this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1));
                var backgroundId = 'background-'+(this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1));
                try{
                    document.getElementById(noteId).style.width = (15.5/this.mySample.timeSubdiv - (8*(100/document.documentElement.clientWidth))) + 'vw';
                    document.getElementById(backgroundId).style.width = (15.5/this.mySample.timeSubdiv - (8*(100/document.documentElement.clientWidth))) + 'vw';
                }
                catch{

                }
            }
        }
    },
    mounted(){
        var backgroundId = 'background-'+(this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1));
        var background = this.$refs[backgroundId];
        var pitch = ("pitch-" + (this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1)));
        var dragItem = this.$refs[pitch];
        if(this.mySample.track[(this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1)-1)].pitch===null){
            this.setTranslate(30, dragItem);
        }
        else{
            this.currentY = -this.mySample.track[(this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1)-1)].pitch/(1200/(60/2)) + 60/2,
            this.initialY = this.currentY,
            this.yOffset = this.currentY,
            this.setTranslate(this.currentY, dragItem);
        }
        if(this.currentY - 30 > 0){
            background.style.top = "40px";
            background.style.transform= `translateY(0px)`;
            background.style.height= Math.abs(this.currentY-30) + "px";
        }
        else{
            background.style.top = "40px";
            background.style.transform= `translateY(${-Math.abs(this.currentY-30)}px)`;
            background.style.height= Math.abs(this.currentY-30) + "px";
        }
        window.addEventListener('resize', this.resizeNote);
    },
    watch:{
        resetChannel(newVal){
            if(newVal){
                this.currentY= 30;
                this.initialY= 30;
                this.yOffset= 30;
                if((this.indexNbSub+this.mySample.timeSubdiv*(this.indexNbTemps-1))===this.mySample.track.length){
                    this.$store.commit("resetChannel", {sampleId: this.mySample.id, newVal: false});
                }
            }
        }
    }
})
</script>

<style scoped>
.item{
    width: 100%;
    background  : rgb(245, 230, 99);
    padding: 2px 0;
    touch-action: none;
    user-select: none;
    border-radius: 5px;
    cursor: ns-resize;
}
</style>