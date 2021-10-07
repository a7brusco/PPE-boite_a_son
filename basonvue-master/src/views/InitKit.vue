<template>
    
</template>

<script>

export default {
    computed:{
        waitKit(){
            if (this.$store.state.initWithKit) {
                this.$router.push('/');
            }
            else {
                setTimeout(this.waitKit, 10);
            }
        }
    },
    props:['id'],
    async mounted(){
        await fetch('https://banana-cobbler-95780.herokuapp.com/api/kit/'+this.id) //don't forget to change the url while dev/prod http://127.0.0.1:8000/api/kit/ or https://banana-cobbler-95780.herokuapp.com/api/kit/
        .then(response => response.json())
        .then(data => {
            var data = JSON.parse(data.samples);
            var sampleList = [];
            data.forEach(sample => {
                sample.fields.file="https://s3.eu-west-3.amazonaws.com/vlmboiteason/static/media/"+sample.fields.file;
                sampleList.push(sample.fields);
            });
            this.$store.commit('initKit',sampleList);
        });
        this.waitKit;
    }
}
</script>