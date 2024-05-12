$(document).ready(function () {

    const jokeButton = document.getElementById("jokeButton");
    const jokeSpinner = document.getElementById("jokeSpinner");
    const audioPlayer = document.getElementById("audioPlayer");
    const audioPlayerGreeting = document.getElementById("audioPlayerGreeting");

    jokeButton.addEventListener("click", async () => {
        audioPlayerGreeting.play();

        let jokeAlert = document.getElementById("jokeAlert");
        jokeAlert.innerHTML = "";
        jokeAlert.hidden = true;

        let topic = document.getElementById("jokeInput").value;
        jokeButton.disabled = true;
        jokeSpinner.hidden = false;

        try {
            const response = await axios.get(`/make-a-joke/${topic}`, { responseType: "blob" });

            if (!response.data) {
                throw new Error("Error fetching audio file");
            }
            const audioBlob = response.data;
            const audioURL = URL.createObjectURL(audioBlob);
            audioPlayer.src = audioURL;
            audioPlayerGreeting.pause();
            audio.currentTime = 0;
            audioPlayer.play();

        } catch (error) {
            if (error.response.status == 429) {

                jokeAlert.innerHTML = "Você já fez muitas requisições, por favor espere 1 minuto para enviar a próxima.";
                jokeAlert.hidden = false;
                audioPlayerGreeting.pause();
                audio.currentTime = 0;
            } else {
                jokeAlert.innerHTML = "Erro no tópico enviado.";
                jokeAlert.hidden = false;
                audioPlayerGreeting.pause();
                audio.currentTime = 0;
            }
        }

        document.getElementById("jokeInput").value = "";

        jokeSpinner.hidden = true;
        jokeButton.disabled = false;

    });
})