// static/main.js

function askQuestion() {
    var queryText = document.getElementById('queryText').value;

    if (queryText.trim() === "") {
        alert("Please enter a question.");
        return;
    }

    var askButton = document.getElementById('askButton');
    askButton.disabled = true;

    var loadingMessage = document.getElementById('loadingMessage');
    loadingMessage.style.display = 'block';

    fetch('/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            queryText: queryText
        })
    })
    .then(response => response.json())
    .then(data => {
        loadingMessage.style.display = 'none';

        var responseArea = document.getElementById('responseArea');
        responseArea.innerHTML = "<p><strong>Server Response:</strong></p><pre>" + data.answer + "</pre>";

        document.getElementById('queryText').value = '';

        // Enable the button after the buffering state (20 seconds)
        setTimeout(() => {
            askButton.disabled = false;
        }, 20000);
    })
    .catch(error => {
        console.error('Error:', error);

        // Hide loading message on error
        loadingMessage.style.display = 'none';

        // Enable the button on error
        askButton.disabled = false;
    });
}        