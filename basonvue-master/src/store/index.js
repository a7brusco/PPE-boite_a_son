import { createStore } from 'vuex'
export default createStore({
  devtools:true,
  state: {
    initWithKit: false,
    kitList: null,
    audioCtx: null,
    limiter: null,
    masterGain: null,
    samples:[],
    samplesChosen: [],
    isPlaying:false,
    previousBpm: 80,
    bpm: 80,
    lookAhead: 10.0,
    loopSeeTime: null,
    scheduleAheadTime: 0.1,
    schedule:[],
    startTime: 0,
    startTimeAutomation:0,
    analyser: null,
    recorder: null,
    record: false,
    endOfRecord: false,
    nbBeatsRecord: 1,
    nbBeatsCurrentRecord: 0,
    isRecording: false,
    optionRecorder: null,
    stream: null,
    chunks: [],
    downloadAvailable: false,
    nbBeats: 4,
    timerAutomation: null,
    oldSourceNodes:[],
    audioJS : require("../assets/js/audio.js"),
  },
  getters: {
    getAudioCtx(state){
      if (state.audioCtx.state==='suspended') {
        state.audioCtx.resume();
      }
      return state.audioCtx;
    },
    getCurrentBeat(state){
      var currentBeat = (state.audioCtx.currentTime - state.startTime)*(state.bpm/60);
      return ((currentBeat%state.nbBeats) +1) ;
    },
  },
  mutations: {
    createAudioCtx(state){
      var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
      state.audioCtx=audioCtx;
      state.masterGain = state.audioCtx.createGain();
      state.analyser = state.audioCtx.createAnalyser();
      state.limiter = state.audioCtx.createDynamicsCompressor();
      state.limiter.attack.setValueAtTime(0,state.audioCtx.currentTime);
      state.limiter.ratio.setValueAtTime(20,state.audioCtx.currentTime);
      state.limiter.threshold.setValueAtTime(-3,state.audioCtx.currentTime);
      state.limiter.release.setValueAtTime(0.05,state.audioCtx.currentTime);
      state.masterGain.connect(state.limiter);
      state.limiter.connect(state.analyser);
      state.analyser.connect(state.audioCtx.destination);
    },
    addDefaultSample(state, buffer){
      state.samples.push({id:1, name: "Default", src:buffer});
      var track = []
      for(var i=0; i<4*state.nbBeats; i++){
        track[i] = {gain: 0, pitch: null, id: i+1};
      }
      var sample = {id:1, name: "Default", src:buffer, timeSubdiv:4, audioNode:null, mute:false, fxParams:{gainValue:1, panValue:0, frequency:20}, track:track, currentNote:0, nextNoteTime:0.0, timerID:null, record:null, 
      drawFilter: false, frequencyInTime: new Array(14*4).fill(20), sliderFreqDisabled: false, QKnobDisabled: false, filterColor: "#333333", filterName : "Bypass", resetChannel: false};
      state.samplesChosen.push(sample);

      //build audio graph
      var source = state.audioCtx.createBufferSource();
      source.buffer = sample.src;
      var gainNode = state.audioCtx.createGain();
      var panNode = state.audioCtx.createStereoPanner();
      var filterNode = state.audioCtx.createBiquadFilter();
      filterNode.type = 'allpass';
      gainNode.connect(panNode);
      panNode.connect(filterNode);
      filterNode.connect(state.masterGain);
      //affect audioNode to sample
      sample.audioNode = {source:source, gain:gainNode, pan:panNode, filter: filterNode};
      //set audioNode value
      sample.audioNode.gain.gain.setValueAtTime(sample.fxParams.gainValue, state.audioCtx.currentTime);
      sample.audioNode.pan.pan.setValueAtTime(sample.fxParams.panValue, state.audioCtx.currentTime);
      sample.audioNode.source.connect(sample.audioNode.gain);
    },
    addSamples(state, {sampleName, buffer}){
      var id = state.samples.length + 1 ;
      var name = sampleName.split('.')[0];
      var sample={name: name, id: id, src:buffer};
      state.samples.push(sample);
    },
    resetChannel(state, {sampleId, newVal}){
      var chosenSample = state.samplesChosen.find(sample => sample.id === sampleId);
      chosenSample.resetChannel = newVal;
    },
    setBpm(state, newBpm){
      state.bpm = newBpm;
    },
    updateNbBeats(state, nbBeats){
      if (isNaN(nbBeats)) {
        nbBeats=1;
      }
      state.samplesChosen.forEach(channel => {
        for (let i = 0; i < channel.timeSubdiv*Math.abs(nbBeats-state.nbBeats); i++) {
          if (nbBeats>state.nbBeats) {
            channel.track.push({gain: 0, pitch: null, id: channel.track.length+1});
          }
          else{
            channel.track.pop({gain: 0, pitch: null, id: channel.track.length+1});
          }
        }
        if(nbBeats>state.nbBeats){
          for(var i=0; i<(nbBeats-state.nbBeats)*14; i++){
            channel.frequencyInTime.push(20);
          }
        }
        else{
          for(var i=0; i<(state.nbBeats- nbBeats)*14; i++){
            channel.frequencyInTime.pop();
          }
        }
      });
      state.nbBeats = nbBeats;
      var width=(16.35*state.nbBeats)+'vw';
      document.querySelector('.divProgress').style.width = width;
    },
    updateNbBeatsRecord(state, newValue){
      state.nbBeatsRecord = newValue;
    },
    addSamplesChosen(state, {sampleName, src}){
      if (state.samplesChosen.length == 0){
        var id = 1;
      }
      else {
        var id = state.samplesChosen[state.samplesChosen.length -1]["id"] + 1;
      }
      var track = []
      for(var i=0; i<4*state.nbBeats; i++){
        track[i] = {gain: 0, pitch: null, id: i+1};
      }
      var sample = {id: id, name: sampleName, src: src, timeSubdiv:4, audioNode:null, mute:false, fxParams:{gainValue:1, panValue:0, frequency: 20}, track:track, currentNote:0, nextNoteTime:0.0, timerID:null, record:null,
      drawFilter: false, frequencyInTime: new Array(14*4).fill(20), sliderFreqDisabled: false, QKnobDisabled:false, filterColor: "#333333",filterName : "Bypass", resetChannel: false};
      //build audio graph
      var source = state.audioCtx.createBufferSource();
      source.buffer = sample.src;
      var gainNode = state.audioCtx.createGain();
      var panNode = state.audioCtx.createStereoPanner();
      var filterNode = state.audioCtx.createBiquadFilter();
      filterNode.type = 'allpass';
      gainNode.connect(panNode);
      panNode.connect(filterNode);
      filterNode.connect(state.masterGain);
      //affect audioNode to sample
      sample.audioNode = {source:source, gain:gainNode, pan:panNode, filter: filterNode};
      //set audioNode value
      sample.audioNode.gain.gain.setValueAtTime(sample.fxParams.gainValue, state.audioCtx.currentTime);
      sample.audioNode.pan.pan.setValueAtTime(sample.fxParams.panValue, state.audioCtx.currentTime);
      sample.audioNode.source.connect(sample.audioNode.gain);
      state.samplesChosen.push(sample);
    },
    deleteSamplesChosen(state, id){
      const wantedSample = state.samplesChosen.find(sample => sample.id === id);
      state.samplesChosen.splice(state.samplesChosen.indexOf(wantedSample), 1);
    },
    resetSamplesChosen(state){
      state.samplesChosen = [] ;
    },
    selectSample(state, {sampleName, sampleId}){
      const wantedSample = state.samples.find(sample => sample.name === sampleName);
      const chosenSample = state.samplesChosen.find(sample => sample.id === sampleId);
      chosenSample.name = wantedSample.name;
      chosenSample.src = wantedSample.src;
    },
    initAudio(state, sampleId){
      const chosenSample = state.samplesChosen.find(sample => sample.id===sampleId);
      if (chosenSample.audioNode === null) {
        var gainNode = state.audioCtx.createGain();
        var panNode = state.audioCtx.createStereoPanner();
        gainNode.connect(panNode);
        panNode.connect(state.masterGain);
        chosenSample.audioNode = {gain:gainNode, pan:panNode};
      }
      chosenSample.audioNode.gain.gain.setValueAtTime(chosenSample.fxParams.gainValue, state.audioCtx.currentTime);
      chosenSample.audioNode.pan.pan.setValueAtTime(chosenSample.fxParams.panValue, state.audioCtx.currentTime);
    },
    activeOnlyThisSong(state, sampleId){
      var reverse = false
      var sample = state.samplesChosen.find(sample => sample.id === sampleId);
      if(sample["mute"]===false){
        for(var i=0; i<state.samplesChosen.length; i++){
          if(state.samplesChosen[i]["id"]!==sampleId){
            if(state.samplesChosen[i]["mute"]===true){
                reverse = true;
              }
              else{
                reverse = false
                break;
              }    
          }
        }
      }
      for(var i=0; i<state.samplesChosen.length; i++){
        if(state.samplesChosen[i]["id"]!==sampleId){
          state.samplesChosen[i]["mute"] = !reverse;
          this.commit("updateGain", {value: document.getElementById("volume" + state.samplesChosen[i]["id"]).value/100, sampleId: state.samplesChosen[i]["id"]});
        }
        else{
          state.samplesChosen[i]["mute"] = false;
          this.commit("updateGain", {value: document.getElementById("volume" + state.samplesChosen[i]["id"]).value/100, sampleId: state.samplesChosen[i]["id"]});
        }
      }
    },
    mute(state, sampleId){
      const chosenSample = state.samplesChosen.find(sample => sample.id===sampleId);
      chosenSample.mute = !chosenSample.mute;
      this.commit("updateGain", {value: document.getElementById("volume" + chosenSample.id).value/100, sampleId: sampleId});
    },
    updateGain(state, {value, sampleId}){
      const chosenSample = state.samplesChosen.find(sample => sample.id===sampleId);
      if(!chosenSample.mute){
        chosenSample.fxParams.gainValue = value;
      }
      else{
        chosenSample.fxParams.gainValue = 0;
      }
      chosenSample.audioNode.gain.gain.setValueAtTime(chosenSample.fxParams.gainValue, state.audioCtx.currentTime);
    },
    updateGainMaster(state, value){
        state.masterGain.gain.setValueAtTime(value, state.audioCtx.currentTime);
    },
    updatePan(state, {value, sampleId}){
      const chosenSample = state.samplesChosen.find(sample => sample.id===sampleId);
      chosenSample.fxParams.panValue = value;
      chosenSample.audioNode.pan.pan.setValueAtTime(chosenSample.fxParams.panValue, state.audioCtx.currentTime);
    },
    playNote(state, {sampleId, gainNote, pitchNote=null}){
      const chosenSample = state.samplesChosen.find(sample => sample.id===sampleId);
      chosenSample.audioNode.source = state.audioCtx.createBufferSource();
      chosenSample.audioNode.source.buffer = chosenSample.src;
      chosenSample.audioNode.gain.gain.setValueAtTime(chosenSample.fxParams.gainValue*gainNote, state.audioCtx.currentTime);
      if(pitchNote!==null){
        chosenSample.audioNode.source.detune.value = pitchNote;
      }
      else{
        chosenSample.audioNode.source.detune.value = 0;
      }
      chosenSample.audioNode.source.connect(chosenSample.audioNode.gain);
      chosenSample.audioNode.source.start();
      state.oldSourceNodes.push(chosenSample.audioNode.source);
    },
    setNote(state, {sampleId, noteId, gainNote}){
      const chosenSample = state.samplesChosen.find(sample => sample.id===sampleId);
      const selectedNote = chosenSample.track.find(note => note.id===noteId);
      selectedNote.gain = gainNote;
    },
    changeTrack(state, {sampleId ,newSubDiv}){
      const chosenSample = state.samplesChosen.find(sample => sample.id===sampleId);
      var track = []
      for(var i=0; i<newSubDiv*state.nbBeats; i++){
        track[i] = {gain: 0, pitch: null, id: i+1};
      }
      chosenSample.track = track;
      chosenSample.timeSubdiv = newSubDiv;
    },
    setPitchNote(state, {valuePitch, max, noteId, sampleId}){
      const chosenSample = state.samplesChosen.find(sample => sample.id===sampleId);
      const selectedNote = chosenSample.track.find(note => note.id===noteId);
      var step = 1200/(max/2)
      selectedNote.pitch = - (valuePitch-max/2)*step;
    },
    nextNote(state, channelId){
      const channel = state.samplesChosen.find(channel => channel.id === channelId);
      const secondsPerBeat = 60.0/(channel.track.length/state.nbBeats*state.bpm);
      channel.nextNoteTime += secondsPerBeat;
      channel.currentNote++;
      if (channel.currentNote === channel.track.length) {
        channel.currentNote = 0;
      }
    },
    initKit(state, sampleList){
      state.kitList = sampleList;
      state.initWithKit = true;
    },
  },
  actions: {
    scheduleNote({commit, dispatch, state}, {beatNumber, time, channelId, record=null}){
      state.schedule.push({note: beatNumber, time: time});
      const channel = state.samplesChosen.find(channel => channel.id === channelId);
      if(record && channel.record===1 && beatNumber===0){
        channel.record = 2; //state 2 ==> end of recording this track 
        var upNbBeatsCurrentRecord = false
        for(var i=0; i<state.samplesChosen.length; i++){
          if(state.samplesChosen[i].record !==2){
            upNbBeatsCurrentRecord = false;
            break;
          }
          else{
            upNbBeatsCurrentRecord = true
          }
        }
        if(upNbBeatsCurrentRecord){
          state.nbBeatsCurrentRecord += 1
          if(state.nbBeatsCurrentRecord===state.nbBeatsRecord){
            state.endOfRecord = true;
          }
          else{
            state.samplesChosen.forEach(channel => {
                channel.record = null;
            })
          }
        }
        if(state.endOfRecord){
          state.recorder.stop();
          dispatch("stop");
          return 0;
        }
      }
      if(record && channel.record===null){
        channel.record = 1; //state 1 ==> start of recording this track
      }
      if (channel.track[beatNumber]["gain"]) {
        if((channel.record===2 && state.record && (state.nbBeatsCurrentRecord+1)===state.nbBeatsRecord) || state.endOfRecord){
        }
        else{
          commit('playNote', {sampleId: channel.id, gainNote: channel.track[beatNumber]["gain"], pitchNote: channel.track[beatNumber]["pitch"]});
        }
      }
    },
    scheduler({state, commit, dispatch}, {channelId, record=null}){
      const channel = state.samplesChosen.find(sample => sample.id === channelId);
      while(channel.nextNoteTime < state.audioCtx.currentTime + state.scheduleAheadTime){
          channel.fxParams.frequency = channel.audioNode.filter.frequency.value;
          dispatch('scheduleNote', {beatNumber: channel.currentNote, time: channel.nextNoteTime, channelId:channel.id, record: record});
          if(state.record && (state.startTime+state.nbBeatsRecord*state.nbBeats*(60/state.bpm))<state.audioCtx.currentTime){
            break;
          }
          else{
            commit('nextNote', channel.id);
          }
      }
      if(state.isPlaying){
        channel.timerID = window.setTimeout(()=>{dispatch('scheduler', {channelId: channel.id, record: record})}, state.lookAhead); //lookAhead = 25.0ms
      }
    },
    loopSeeTime({state, getters, dispatch}){
      if(state.isPlaying){
          var progressBar = document.getElementById("progress");
          const currentBeat = getters.getCurrentBeat;
          progressBar.style.width = (((currentBeat - 1)/state.nbBeats)*100) + "%";
      }
      else if(state.record===false && state.isPlaying===false){
        document.getElementById("progress").style.width = "0%";
      }
      state.loopSeeTime = window.requestAnimationFrame(() => {
          dispatch('loopSeeTime');
      });
    },
    play({state,commit, dispatch}, record=null){
      state.oldSourceNodes.forEach(oldSourceNode => {
        oldSourceNode.stop();
      });
      state.isPlaying=true;
      document.getElementById("bpm").disabled = true;
      document.getElementById("inputButtonUp").disabled = true;
      document.getElementById("inputButtonDown").disabled = true;
      document.getElementById("bpmGroup").style.opacity = 0.5;
      document.getElementById("nbBeats").disabled = true;
      document.getElementById("inputButtonUpNbBeats").disabled = true;
      document.getElementById("inputButtonDownNbBeats").disabled = true;
      document.getElementById("nbBeatsGroup").style.opacity = 0.5;
      state.startTime = state.audioCtx.currentTime;
      state.startTimeAutomation = state.audioCtx.currentTime + 0.1;
      dispatch("automation", {time: state.audioCtx.currentTime+0.1, point: 0, timeAutomation:state.audioCtx.currentTime+0.1});
      state.samplesChosen.forEach(channel => {
        channel.sliderFreqDisabled = true; 
        channel.QKnobDisabled = true;
        //channel.nextNoteTime = state.audioCtx.currentTime;
        channel.nextNoteTime = state.audioCtx.currentTime + 0.1;
        dispatch('scheduler', {channelId: channel.id, record: record});
        window.requestAnimationFrame(() => {
          dispatch('loopSeeTime');
        });
      });
      var selects = document.getElementsByName("select")
      for(var i=0; i<selects.length; i++){
        selects[i].disabled= true;
        selects[i].style.backgroundColor = "#888";
      }
    },
    stop({state}){
      state.isPlaying = false;
      window.cancelAnimationFrame(state.loopSeeTime);
      document.getElementById("bpm").disabled = false;
      document.getElementById("inputButtonUp").disabled = false;
      document.getElementById("inputButtonDown").disabled = false;
      document.getElementById("bpmGroup").style.opacity = 1;
      document.getElementById("nbBeats").disabled = false;
      document.getElementById("inputButtonUpNbBeats").disabled = false;
      document.getElementById("inputButtonDownNbBeats").disabled = false;
      document.getElementById("nbBeatsGroup").style.opacity = 1;
      var selects = document.getElementsByName("select")
      for(var i=0; i<selects.length; i++){
        selects[i].disabled= false;
        selects[i].style.backgroundColor = "#FFF";
      }
      window.clearTimeout(state.timerAutomation);
      state.samplesChosen.forEach(channel => {
        channel.audioNode.filter.frequency.cancelScheduledValues(state.audioCtx.currentTime);
        channel.sliderFreqDisabled = false;
        channel.QKnobDisabled = false;
        window.clearTimeout(channel.timerID);
        channel.currentNote = 0;
        channel.nextNoteTime = 0.0;
        var freq = parseFloat(document.getElementById("freq" + channel.id).value);
        freq = (Math.pow(10,freq)*20).toFixed(0);
      });
      state.oldSourceNodes.forEach(oldSourceNode => {
        oldSourceNode.stop();
      });
    },
    automation({state, dispatch}, {time, point, timeAutomation}){
      if(point >= 14*state.nbBeats){
        state.startTimeAutomation += state.nbBeats*(60/state.bpm);
        point = 0;
      }
      if(timeAutomation-state.startTimeAutomation> point*(60/state.bpm)*(1/14)){
        state.samplesChosen.forEach(channel => {
            channel.audioNode.filter.frequency.setValueAtTime(channel.frequencyInTime[point], time);
        });
        point+=1;
        time+=(60/state.bpm)*(1/14);
      }
      if(state.isPlaying){
        state.timerAutomation = window.setTimeout(()=>{dispatch('automation', {time: time, point: point, timeAutomation: timeAutomation+state.lookAhead})}, state.lookAhead);
      }
    },
    startRecord({state, dispatch}){
      if(state.audioCtx.state=="suspended"){
        state.audioCtx.resume();
      }
      if(!state.record){
        if(state.isPlaying){
          dispatch('stop');
          document.getElementById("btnPause").classList.add("d-none");
          document.getElementById("btnPlay").classList.remove("d-none");
        }
        document.getElementById("btnPlay").disabled = true;
        document.getElementById("btnPause").disabled = true;
        //document.getElementById("recorderButton").disabled = true;
        document.getElementById("circleRecord").style.fill="red";
        state.stream = state.audioCtx.createMediaStreamDestination();
        state.limiter.disconnect();
        state.recorder = new MediaRecorder(state.stream.stream, {mimeType: "audio/webm;codecs=opus"});
        state.record = true;
        state.limiter.connect(state.stream);
        state.recorder.start();
        dispatch('play', true);
        state.recorder.ondataavailable = function(e){
          state.chunks.push(e.data);
        }
        state.recorder.onstop = async function(evt) {
          state.nbBeatsCurrentRecord = 0;
          state.record = false;
          //var blob = new Blob(state.chunks, { 'type' : 'audio/wav' });
          var arrayBuffer = await state.audioJS.readUploadedFile(state.chunks[0]);
          var audioBuffer = await state.audioJS.createAudioBuffer(arrayBuffer, state.audioCtx);
          var fileURL = state.audioJS.bufferToWave(audioBuffer, 0, audioBuffer.length, 16);
          state.downloadAvailable = true;
          var audioElement = document.getElementById('saveRecordFileA');
          audioElement.setAttribute("href",fileURL);
          //audioElement.setAttribute("href",URL.createObjectURL(state.chunks[0]));
          document.getElementById("saveFileNameRecord").click();
          state.limiter.disconnect();
          state.limiter.connect(state.analyser);
          state.chunks = [];
          document.getElementById("btnPlay").disabled = false;
          document.getElementById("btnPause").disabled = false;
          //document.getElementById("recorderButton").disabled = false;
          document.getElementById("circleRecord").style.fill="white";
          document.getElementById("progress").style.width = "0%";
          state.samplesChosen.forEach(channel => {
            channel.record = null;
          });
          state.endOfRecord = false;
        };
      }
    },
  },
  modules: {
  }
})
