<template>
<div id="container" :ref="'container-'+idPoint" style="height: inherit; width: 10%"
        @mousedown="dragStart" 
        @mouseup="dragEnd" 
        @mousemove="drag"
        @mouseout="makeMouseOutFn">
    <div style="width:100%; height: 5px; cursor:ns-resize;" :ref="'automation'+mySample.id+idPoint" :style="{backgroundColor: mySampleColor}">
    </div>
    <div :ref="'background-automation-'+mySample.id+idPoint" style="position: relative; top:295px; opacity: 0.2; width: 100%;" :style="{backgroundColor: mySampleColor, height: Math.abs(295-currentY) + 'px'}">
    </div>
</div>
</template>

<script>

export default ({
    data(){
        return{
            activeDrag: false,
            currentY: null,
            initialY: null,
            yOffset: null,
            automation: false,
            filterDrawPoint: null,
            frequency: null,
        };
    },
    props:['id', 'idPoint', 'x', 'y', 'freqInitial'],
    computed:{
        mySample(){
            const chosenSample = this.$store.state.samplesChosen.find(sample => sample.id===this.id);
            if(chosenSample){
                return chosenSample;
            }
        },
        mySampleColor(){
            const chosenSample = this.$store.state.samplesChosen.find(sample => sample.id===this.id);
            if(chosenSample){
                return chosenSample.filterColor;
            }
        },
        drawFilterChange(){
            if(this.mySample !== undefined){
                return this.mySample.drawFilter;
             }
        },
        frequencyChange(){
            if(this.mySample !== undefined){
                return this.mySample.fxParams.frequency;
            }
        }
    },
    methods:{
        dragStart(e){
            var automation = ("automation"+this.mySample.id+this.idPoint);
            var dragItem = this.$refs[automation];
            if (e.type === "touchstart") {
                this.initialY = e.touches[0].clientY - this.yOffset;
            } else {
                this.initialY = e.clientY - this.yOffset;
            }
            if (e.target === dragItem) {
                if (window.event.ctrlKey) {
                    this.dragClick(e);
                }
                else{
                    var containerGlobal = document.getElementById("containerAutomation");
                    containerGlobal.style.cursor = "ns-resize";
                    this.activeDrag = true;
                    this.automation = true;
                }
            }
            if(e && this.activeDrag === false){
                this.mySample.drawFilter = true;
                this.dragClick(e);
            }
            
        },
        dragEnd(e) {
            if(e){
                this.mySample.drawFilter = false;
            }
            var containerGlobal = document.getElementById("containerAutomation");
            containerGlobal.style.cursor = "initial";
            this.initialY = this.currentY;
            this.activeDrag = false;
        },
        drag(e){
            var automation = ("automation"+this.mySample.id+this.idPoint);
            var dragItem = this.$refs[automation];
            var backgroundId = ('background-automation-'+this.mySample.id+this.idPoint);
            var background = this.$refs[backgroundId];
            if (this.activeDrag){
                e.preventDefault();
                if((e.clientY - this.initialY)<=(300-parseInt(dragItem.style.height.split("p"))) && (e.clientY - this.initialY)>=0){
                    this.currentY = e.clientY - this.initialY;
                    background.style.transform= `translateY(${-Math.abs(296-this.currentY)}px)`;
                    background.style.height= Math.abs(295-this.currentY) + "px";
                }
                this.yOffset = this.currentY;
                this.setTranslate(this.currentY, dragItem);
                this.frequency =  (Math.pow(10,(3-(this.currentY/98.33)))*20).toFixed(0);
                this.mySample.frequencyInTime[this.idPoint-1] = parseInt(this.frequency);
            }
        },
        dragClick(e){
            if(this.mySample.drawFilter){
                var automation = ("automation"+this.mySample.id+this.idPoint);
                var dragItem = this.$refs[automation];
                var backgroundId = ('background-automation-'+this.mySample.id+this.idPoint);
                var background = this.$refs[backgroundId];
                var containerId = ('container-'+this.idPoint);
                var container = this.$refs[containerId];
                var channelSample = document.getElementById("channelSample");
                var posX = e.clientX-container.offsetLeft-window.scrollX+channelSample.scrollLeft+(this.idPoint-1)*dragItem.clientWidth-channelSample.offsetParent.offsetLeft;
                var posY = e.clientY+window.scrollY-container.offsetTop+channelSample.scrollTop-channelSample.offsetParent.offsetTop;
                if(posX < ((this.idPoint-1)*dragItem.clientWidth+dragItem.clientWidth) &&  posX > (this.idPoint-1)*dragItem.clientWidth){
                    e.preventDefault();
                    if(posY<=(300-parseInt(dragItem.style.height.split("p"))) && posY>=0){
                        this.currentY = posY;
                        background.style.transform= `translateY(${-Math.abs(296-this.currentY)}px)`;
                        background.style.height= Math.abs(295-this.currentY) + "px";
                    }
                    this.yOffset = this.currentY;
                    this.setTranslate(this.currentY, dragItem);
                    this.frequency =  (Math.pow(10,(3-(this.currentY/98.33)))*20).toFixed(0);
                    this.mySample.frequencyInTime[this.idPoint-1] = parseInt(this.frequency);
                    if (window.event.ctrlKey) {
                        this.mySample.fxParams.frequency = this.frequency; 
                    }
                }
                if(posX<0 || posX>(this.$store.state.nbBeats*14*dragItem.clientWidth+12) || posY<0 || posY>parseInt(document.getElementById("containerAutomation").style.height.split("p")[0])){
                    console.log(posX, (this.$store.state.nbBeats*14*dragItem.clientWidth));
                    if(this.mySample.drawFilter){
                        this.mySample.drawFilter = false;
                    }
                }
            }
        },
        setTranslate(yPos, el) {
            el.style.transform = "translate3d(" + 0 + "px, " + yPos + "px, 0)";
        },
        makeMouseOutFn(e){
            var containerId = 'container-'+this.idPoint;
            var container = this.$refs[containerId];
            var backgroundId = ('background-automation-'+this.mySample.id+this.idPoint);
            var background = this.$refs[backgroundId];
            var list = this.traverseChildren(container);
            list.push(this.traverseChildren(background));
            var event = e.toElement || e.relatedTarget;
            if (!!~list.indexOf(event)) {
                return;
            }
            this.dragEnd();
        },   
        traverseChildren(elem){
            var children = [];
            var q = [];
            q.push(elem);
            while (q.length > 0) {
            var elem = q.pop();
            children.push(elem);
            pushAll(elem.children);
            }
            function pushAll(elemArray){
            for(var i=0; i < elemArray.length; i++) {
                q.push(elemArray[i]);
            }
            }
            return children;
        },
    },
    watch: {
        drawFilterChange(newVal){
            if(newVal){
                window.addEventListener('mousemove', this.dragClick, false);
            }
            else{
                 window.removeEventListener('mousemove', this.dragClick, false);
            }
        },
        frequencyChange(newVal){
            if(window.event !== undefined && this.mySample !== undefined){
                if (window.event.ctrlKey) {
                    var automation = ("automation"+this.mySample.id+this.idPoint);
                    var dragItem = this.$refs[automation];
                    this.frequency = newVal
                    this.currentY = (3-Math.log10(newVal/20))*98.33;
                    this.mySample.frequencyInTime[this.idPoint-1] = parseInt(newVal);
                    this.initialY= this.currentY,
                    this.yOffset= this.currentY,
                    this.setTranslate(this.currentY, dragItem);
                    var backgroundId = ('background-automation-'+this.mySample.id+this.idPoint);
                    var background = this.$refs[backgroundId];
                    background.style.transform= `translateY(${-Math.abs(295-this.currentY)}px)`;
                    background.style.height= Math.abs(295-this.currentY) + "px";
                }
            }
        }
    },
    mounted(){
        var automation = ("automation"+this.mySample.id+this.idPoint);
        var dragItem = this.$refs[automation];
        this.currentY= this.y,
        this.initialY= this.y,
        this.yOffset= this.y,
        this.setTranslate(this.y, dragItem);
        var backgroundId = ('background-automation-'+this.mySample.id+this.idPoint);
        var background = this.$refs[backgroundId];
        background.style.transform= `translateY(${-Math.abs(295-this.currentY)}px)`;
        background.style.height= Math.abs(295-this.currentY) + "px";
    },
})
</script>

<style scoped>

</style>
