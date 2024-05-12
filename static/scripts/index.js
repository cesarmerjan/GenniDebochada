$(document).ready(function () {

    const jokeButton = document.getElementById("jokeButton");
    const audioPlayer = document.getElementById("audioPlayer");
    const jokeSpinner = document.getElementById("jokeSpinner");

    jokeButton.addEventListener("click", async () => {
        let jokeAlert = document.getElementById("jokeAlert")
        jokeAlert.innerHTML = ""
        jokeAlert.hidden = true

        let topic = document.getElementById("jokeInput").value
        jokeButton.disabled = true
        jokeSpinner.hidden = false

        let spinner = document.createElement("jokeSpinner")

        try {
            const response = await axios.get(`/make-a-joke/${topic}`, { responseType: "blob" });

            if (!response.data) {
                throw new Error("Error fetching audio file");
            }
            const audioBlob = response.data;
            const audioURL = URL.createObjectURL(audioBlob);
            audioPlayer.src = audioURL;
            audioPlayer.play();

        } catch (error) {
            jokeAlert.innerHTML = "Erro no tópico enviado."
            jokeAlert.hidden = false
        }

        document.getElementById("jokeInput").value = ""

        jokeSpinner.hidden = true
        jokeButton.disabled = false

    });
})