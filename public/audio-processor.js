// AudioWorkletProcesor that sends input audio to the backend, 
// sending chunks of 2048 samples at a time

class AudioProcessor extends AudioWorkletProcessor {
    constructor() {
        super();

        this.bufferSize = 2048
        this.buffer = new Float32Array(this.bufferSize); // each sample is a float32, i.e. 4 bytes
        this.bufferIndex = 0;
    }
    process(inputs, outputs, parameters) {
        // first channel of the first input
        const audioData = inputs[0][0]; // this should 128 samples

        if (!audioData) return true;

        // fills buffer, then sends audio data message up to the main thread when full
        this.buffer.set(audioData, this.bufferIndex);
        this.bufferIndex += audioData.length;
        if (this.bufferIndex >= this.bufferSize) {
            this.port.postMessage(this.buffer.slice());
            this.bufferIndex = 0;
        }

        return true;
    }
}

registerProcessor("audio-processor", AudioProcessor);