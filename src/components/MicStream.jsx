import { useRef, useEffect } from 'react';
export default function MicStream() {
    const playerRef = useRef(null);
    const wsRef = useRef(null);
    const count = useRef(0);

    useEffect(async () => {
        await navigator.mediaDevices.getUserMedia({audio: true, video: false}).then(
            (stream) => {
                if (playerRef.current) {
                    playerRef.current.srcObject = stream;
                }
            }
        )
    }, [])

    // websocket
    const ws = new WebSocket("ws://localhost:8000/projects/audio");
    ws.onmessage = (e) => {
        if (wsRef.current) {
            wsRef.current.innerHTML = e.data;
        }
    }

    const handleInput = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        // send file to backend
        const data = new FormData();
        data.append("file", file);
        const request = new Request("http://localhost:8000/audio", {
            method: "POST",
            body: data
        })

        try {
            const response = await fetch(request)
            if (!response.ok) {
                throw new Error(`Post error status: ${response.status}`);
            }
            console.log("Post successful");
            const result = await response.blob(); // result is the edited audio file

            if (playerRef.current) {
                playerRef.current.src = URL.createObjectURL(result);
            }
        } catch (error) {
            throw new Error(`Fetch error: ${error}`);
        }
    }

    async function handleButtonClick() {
        console.log("Button clicked!");
        ws.send(`sent package ${count.current}`);
        count.current++;
    };

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
};