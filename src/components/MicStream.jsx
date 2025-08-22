export default function MicStream() {
    const handleInput = (e) => {
        const file = e.target.files[0];
        const url = URL.createObjectURL(file);
        // transforms
        const player = document.getElementById("player");
        player.src = url;
        console.log("done");
    }

    return (
        <div>
            <input id="recorder" type="file" accept="audio/*" onChange={handleInput} capture />
            <audio id="player" controls></audio>
        </div>
    )
};