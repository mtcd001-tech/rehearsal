/* Convert microphone frames to mono 16 kHz PCM without monitoring the mic. */
class InterviewPCM extends AudioWorkletProcessor {
 constructor(){super();this.sum=0;this.count=0;this.phase=0;this.packet=[];}
 process(inputs){
  const channel=inputs[0]?.[0];if(!channel)return true;
  const ratio=sampleRate/16000;
  for(const sample of channel){this.sum+=sample;this.count++;this.phase++;
   if(this.phase>=ratio){const x=Math.max(-1,Math.min(1,this.sum/this.count));this.packet.push(x<0?x*32768:x*32767);this.phase-=ratio;this.sum=0;this.count=0;}
   if(this.packet.length>=1600){const pcm=new Int16Array(this.packet);this.port.postMessage(pcm.buffer,[pcm.buffer]);this.packet=[];}
  }return true;
 }
}
registerProcessor('interview-pcm',InterviewPCM);
