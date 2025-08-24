import { useRef} from 'react';

export default function MicStream() {
    const playerRef = useRef(null);

    const handleInput = (e) => {
        const file = e.target.files[0];
        const url = URL.createObjectURL(file);

        if (playerRef.current) {
            playerRef.current.src = url
        }

        // send file to backend
        const data = new FormData();
        data.append("file", file)
        const xhr = new XMLHttpRequest();

        xhr.onload = (e) => {
            console.log("transaction completed");
            console.log(xhr.responseText);
        }

        xhr.open("POST", "http://localhost:8000/test");
        xhr.send(data);
    }

    const handleButtonClick = () => {
        console.log("Button clicked!");
    };

    return (
        <div>
            <div className="p-5">
                <button onClick={handleButtonClick}>
                    Click me
                </button>
            </div>
            <input id="recorder" type="file" accept="audio/*" onChange={handleInput} capture />
            <audio ref={playerRef} controls></audio>
        </div>
    )
};