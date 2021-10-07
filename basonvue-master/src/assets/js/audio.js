export async function createAudioBuffer(arrayBuffer, audioCtx){
    return new Promise((resolve, reject) => {
      audioCtx.decodeAudioData(arrayBuffer, resolve, reject);
    });
}
export function readUploadedFile(file) {
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
}

export function bufferToWave(abuffer, offset, len, bitdepth) {
    // Convert a audio-buffer segment to a Blob using WAVE representation
    // The returned Object URL can be set directly as a source for an Auido element.
    // (C) Ken Fyrstenberg / MIT license
  
    function setUint16(data) {
      view.setUint16(pos, data, true);
      pos += 2;
    }
    
    function setUint32(data) {
      view.setUint32(pos, data, true);
      pos += 4;
    }

    function setSample(data, bitdepth) {
      if (bitdepth==16) {
        view.setInt16(pos, data, true);
        pos+=2;
      } else if (bitdepth==32) {
        view.setInt32(pos, data, true);
        pos+=4;
      } else {
        firstByte = data & 0x000000ff;
        secondByte = (data & 0x0000ff00)>>8;
        thirdByte = (data & 0x00ff0000)>>16;
        view.setInt8(pos, firstByte, true);
        view.setInt8(pos+1, secondByte, true);
        view.setInt8(pos+2, thirdByte, true);
        pos+=3;
      }
    }

    var numOfChan = abuffer.numberOfChannels,
        length = len * numOfChan * bitdepth/8 + 44,
        buffer = new ArrayBuffer(length),
        view = new DataView(buffer),
        channels = [], i, sample,
        pos = 0;
        
      // write WAVE header
      setUint32(0x46464952);                         // "RIFF"
      setUint32(length - 8);                         // file length - 8
      setUint32(0x45564157);                         // "WAVE"
      setUint32(0x20746d66);                         // "fmt " chunk
      setUint32(16);                                 // length = 16
      setUint16(1);                                  // PCM (uncompressed)
      setUint16(numOfChan);
      setUint32(abuffer.sampleRate);
      setUint32(abuffer.sampleRate * bitdepth/8 * numOfChan); // avg. bytes/sec
      setUint16(numOfChan * bitdepth/8);             // block-align
      setUint16(bitdepth);                           // 16-bit or 24-bit commonly
      setUint32(0x61746164);                         // "data" - chunk
      setUint32(length - pos - 4);                   // chunk length

    // write interleaved data
    for(i = 0; i < abuffer.numberOfChannels; i++)
      channels.push(abuffer.getChannelData(i));
    
      while(pos < length) {
        for(i = 0; i < numOfChan; i++) {             // interleave channels
          sample = Math.max(-1, Math.min(1, channels[i][offset])); // clamp
          sample = (0.5 + sample < 0 ? sample * Math.pow(2,bitdepth-1) : sample * (Math.pow(2,bitdepth-1)-1))|0; // scale to 16-bit/24-bit signed int
          setSample(sample, bitdepth);               //update chunk
        }
        offset++                                     // next source sample
    }

    // create Blob
    return (URL || webkitURL).createObjectURL(new Blob([buffer], {type: "audio/wav"}));
  }