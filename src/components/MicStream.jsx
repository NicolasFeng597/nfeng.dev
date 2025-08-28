import { useRef, useEffect } from 'react';
export default function MicStream() {
    const playerRef = useRef(null);
    const wsRef = useRef(null);
    const count = useRef(0);
    const recorder = useRef(null);
    const streamRef = useRef(null);

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
                    sampleRate: 22050,
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

    // const handleInput = async (e) => {
    //     const file = e.target.files[0];
    //     if (!file) return;

    //     // send file to backend
    //     const data = new FormData();
    //     data.append("file", file);
    //     const request = new Request("http://localhost:8000/audio", {
    //         method: "POST",
    //         body: data
    //     })

    //     try {
    //         const response = await fetch(request)
    //         if (!response.ok) {
    //             throw new Error(`Post error status: ${response.status}`);
    //         }
    //         console.log("Post successful");
    //         const result = await response.blob(); // result is the edited audio file

    //         if (playerRef.current) {
    //             playerRef.current.src = URL.createObjectURL(result);
    //         }
    //     } catch (error) {
    //         throw new Error(`Fetch error: ${error}`);
    //     }
    // }

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