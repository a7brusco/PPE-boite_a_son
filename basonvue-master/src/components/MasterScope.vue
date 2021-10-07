<template>
<div style="display: block; position: relative">
    <span class="analyser">ANALYSER SCOPE (FREQUENCY IN HZ)</span>
    <div class="master" style="display: flex; border: 2px solid rgb(96, 100, 105); border-radius: 0.5rem; padding: 1.6em ">
        <div style="width: 931px;" >
            <div>
                <canvas width="931" height="150" id="waveform" style="padding: 0; display: block">
                </canvas>
            </div>
            <div style="display:flex; margin-top: -1px;">
                <div class="verticalLine" style="margin-left: 1 px"></div>
                <div class="verticalLine" style="margin-left: 45px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
                <div class="verticalLine" style="margin-left: 45.5px"></div>
            </div>
            <div style="display:flex; color: ghostwhite; margin-top: 4px; height: 20px">
                <p style="margin-left: -10px">20</p>
                <p style='margin-left: 29px;'>1k</p>
                <p style='margin-left: 29.5px'>2k</p>
                <p style='margin-left: 29.5px'>3k</p>
                <p style='margin-left: 29.5px'>4k</p>
                <p style='margin-left: 29.5px'>5k</p>
                <p style='margin-left: 29.5px'>6k</p>
                <p style='margin-left: 29.5px'>7k</p>
                <p style='margin-left: 29.5px'>8k</p>
                <p style='margin-left: 29.5px'>9k</p>
                <p style='margin-left: 29.5px'>10k</p>
                <p style='margin-left: 20.5px'>11k</p>
                <p style='margin-left: 20.5px'>12k</p>
                <p style='margin-left: 20.5px'>13k</p>
                <p style='margin-left: 20.5px'>14k</p>
                <p style='margin-left: 20.5px'>15k</p>
                <p style='margin-left: 20.5px'>16k</p>
                <p style='margin-left: 20.5px'>17k</p>
                <p style='margin-left: 20.5px'>18k</p>
                <p style='margin-left: 20.5px'>19k</p>
                <p style='margin-left: 20.5px'>20k</p>
            </div>
        </div>
    </div>
</div>
</template>


<script>
export default {
    methods:{
        
        /*drawWaveform(){
            const width = 800;
            const height = 100;
            var canvas = document.getElementById("waveform");   
            var canvasCtx = canvas.getContext('2d');
            if(this.$store.state.isPlaying){
                this.$store.state.analyser.fftSize = 2048;
                var bufferLength = this.$store.state.analyser.frequencyBinCount;
                var dataArray = new Uint8Array(bufferLength);
                canvasCtx.clearRect(0, 0, width, height);
                this.$store.state.analyser.getByteTimeDomainData(dataArray);
                canvasCtx.fillStyle = 'rgb(200, 200, 200)';
                canvasCtx.fillRect(0, 0, width, height);
                canvasCtx.lineWidth = 2;
                canvasCtx.strokeStyle = 'rgb(0, 0, 0)';
                canvasCtx.beginPath();      
                var sliceWidth = width * 1.0 / bufferLength;
                var x = 0;
                for(var i = 0; i < bufferLength; i++) {
                    var v = dataArray[i] / 128.0;
                    var y = v * height/2;
                    if(i === 0) {
                    canvasCtx.moveTo(x, y);
                    } else {
                    canvasCtx.lineTo(x, y);
                    }
                    x += sliceWidth;
                }
                canvasCtx.lineTo(canvas.width, canvas.height/2);
                canvasCtx.stroke();
            }
            else{
                canvasCtx.fillStyle = 'rgb(200, 200, 200)';
                canvasCtx.fillRect(0, 0, width, height);
                canvasCtx.lineWidth = 2;
                canvasCtx.strokeStyle = 'rgb(0, 0, 0)';
                canvasCtx.beginPath();     
                for(var i = 0; i < width; i++) {
                    if(i === 0) {
                    canvasCtx.moveTo(i, height/2);
                    } else {
                    canvasCtx.lineTo(i, height/2);
                    }
                }
                canvasCtx.lineTo(canvas.width, canvas.height/2);
                canvasCtx.stroke();
            }
            this.drawWaveformRequest = requestAnimationFrame(this.drawWaveform);
        },*/
        drawFrequencyBar(){
            var canvas = document.getElementById("waveform");   
            var canvasCtx = canvas.getContext('2d');
            if(this.$store.state.analyser){
                this.$store.state.analyser.fftSize = 2048;
                var bufferLength = this.$store.state.analyser.frequencyBinCount;
                var dataArray = new Uint8Array(bufferLength);
                this.$store.state.analyser.getByteFrequencyData(dataArray);
                canvasCtx.fillStyle = 'rgb(0, 0, 0)';
                canvasCtx.fillRect(0, 0, canvas.width, canvas.height);
                var barWidth = 0.5;//(canvas.width / (bufferLength))*2.5-1;
                var barHeight;
                var x = 0;
                for(var i = 0; i < bufferLength; i++) {
                    barHeight = dataArray[i];
                    canvasCtx.fillStyle = 'rgb(' + (barHeight+100) + ',50,50)';
                    canvasCtx.fillRect(x,canvas.height-barHeight/2,barWidth,barHeight);
                    x += barWidth + 0.5;
                }
            }
            this.drawFrequencyBarRequest = requestAnimationFrame(this.drawFrequencyBar);
        },
        /*toggleTimeFrequency(){
            if(this.drawFrequencyBarRequest){
                window.cancelAnimationFrame(this.drawFrequencyBarRequest);
                this.drawFrequencyBarRequest = null;
                requestAnimationFrame(this.drawWaveform);
            }
            else{
                window.cancelAnimationFrame(this.drawWaveformRequest);
                this.drawWaveformRequest = null;
                requestAnimationFrame(this.drawFrequencyBar);
            }
        },*/
    },
    mounted(){
        var canvas = document.getElementById("waveform");   
        var canvasCtx = canvas.getContext('2d');
        canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
        this.drawFrequencyBar();
    }
}

</script>

<style scoped>
.master{
    display: grid; 
    width: 100%; 
    grid-template-columns: 8rem 8rem auto; 
    align-items: start;
}
.verticalLine {
  border-left: 1px solid #ffffff;
  height: 7px;
}
.analyser{
    border-radius: 1em;
    color: rgb(144, 149, 153);
    background-color: rgb(32, 36, 39);
    font-weight: 600;
    font-size: 0.6rem;
    margin: 0px;
    padding: 0px 4px;
    position: absolute;
    left: 0.5rem;
    top: -0.4em;
    letter-spacing: 0.1em;
    border-radius: 3px;
    line-height: 1em;
    display: block;
}
@media (max-width: 1300px){
    .master{
        display: block;
    }
    /*#waveform{
        margin-top:20px;
        margin-left: -250px;
    }*/
}
@media (max-width: 900px){
    /*#waveform{
        width: 75vw;
        height: 100px;
    }*/
}
</style>