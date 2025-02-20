document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('form').onsubmit = function () {

        const text = document.querySelector('input[name="text"]').value;
        const formData = { text: text };  // ✅ JSON object instead of FormData

        fetch('/check_hate', {  // ✅ Corrected to send request to /check_hate
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.result) {
                alert('No hate speech detected.');
            } else {
                alert('Hate speech detected!');
            }
        })
        .catch(error => {
            console.error('There was an error!', error);
        });

        return false; // Prevent default form submission
    };
});
