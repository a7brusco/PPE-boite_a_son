<template>
    <label for="sample" class="btn btn-secondary btn-style" style="width: 190px; display: flex;">
        <div style="margin-top:3px">
            <p style="margin: 5px 15px 0 0px">ADD SAMPLES</p>
        </div>
        <div>
            <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="bi bi-music-note-list" viewBox="0 0 16 16" style="margin-top:3px">
                <path d="M12 13c0 1.105-1.12 2-2.5 2S7 14.105 7 13s1.12-2 2.5-2 2.5.895 2.5 2z"/>
                <path fill-rule="evenodd" d="M12 3v10h-1V3h1z"/>
                <path d="M11 2.82a1 1 0 0 1 .804-.98l3-.6A1 1 0 0 1 16 2.22V4l-5 1V2.82z"/>
                <path fill-rule="evenodd" d="M0 11.5a.5.5 0 0 1 .5-.5H4a.5.5 0 0 1 0 1H.5a.5.5 0 0 1-.5-.5zm0-4A.5.5 0 0 1 .5 7H8a.5.5 0 0 1 0 1H.5a.5.5 0 0 1-.5-.5zm0-4A.5.5 0 0 1 .5 3H8a.5.5 0 0 1 0 1H.5a.5.5 0 0 1-.5-.5z"/>
            </svg>
        </div>
    </label>
    <input type="file" accept="audio/*" id="sample" @change="addSampleOption" multiple>
</template>

<script>
export default {

    computed:{
        getAudioCtx(){
            return this.$store.getters.getAudioCtx;
        },
    },
    methods:{
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
        async addSampleOption(){
            var fileList = document.getElementById("sample").files;
            for (let i = 0; i < fileList.length; i++) {
                const sampleFile = fileList[i];
                var arrayBuffer = await this.readUploadedFile(sampleFile);
                var buffer = await this.createAudioBuffer(arrayBuffer);
                this.$store.commit('addSamples',{sampleName:sampleFile.name,buffer:buffer});
            }
        },
    },
}
</script>

<style scoped>

input{
    display: none;
}
.btn{
    box-shadow: none !important;
    height: 52px;
}
.btn-style{
    background: rgba(217, 83, 79, 0) linear-gradient(190deg, rgb(25, 25, 29) 0%, rgb(48, 48, 54) 50%, rgb(10, 14, 10) 51%, rgb(41, 41, 45) 100%) repeat scroll 0% 0%;
    border-width: 2px;
}
</style>