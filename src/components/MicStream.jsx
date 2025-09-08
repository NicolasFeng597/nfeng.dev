import { useRef, useEffect } from 'react';
export default function MicStream() {
    const playerRef = useRef(null);
    const wsRef = useRef(null);
    const count = useRef(0);
    const recorder = useRef(null);
    const streamRef = useRef(null);
    const sampleRate = 22050;

    useEffect(() => {
        const setup = async () => {
            // get mic stream
            let stream;
            try {
                stream = await navigator.mediaDevices.getUserMedia({audio: true, video: false});
            } catch (error) {
                console.error("Error setting up recorder:", error);
                return;
            }

            // websocket init
            const ws = new WebSocket("ws://localhost:8000/projects/audio");
            ws.onmessage = (e) => {
                if (wsRef.current) {
                    count.current++;
                    wsRef.current.innerHTML = `received ${count} datas`;
                }
            }

            // setting playback audio element TODO: remove
            streamRef.current = stream;
            
            if (playerRef.current) {
                playerRef.current.srcObject = stream;
            }
            
            // AudioContext for sending audio to the backend
            try {
                const audioContext = new AudioContext({
                    sampleRate: sampleRate,
                });
                await audioContext.audioWorklet.addModule("/audio-processor.js");
                const source = audioContext.createMediaStreamSource(stream);
                const processor = new AudioWorkletNode(audioContext, "audio-processor");
                
                // receives audio data message from the processor
                processor.port.onmessage = (e) => {
                    if (e.data) ws.send(e.data);
                }

                source.connect(processor);
            } catch (e) {
                console.error(`Error setting up audio context: ${e}`);
            }
        }

        setup();
    }, []);

    function handleButtonClick() {
        console.log("Button clicked!");
    }

    return (
        <div>
            <div className="p-5">
                <button onClick={handleButtonClick}>
                    Click me
                </button>
                <p ref={wsRef}></p>
            </div>
            <audio ref={playerRef} controls></audio>
        </div>
    )
}