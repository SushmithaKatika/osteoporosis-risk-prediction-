document.getElementById('prediction-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    var formData = new FormData(this);
    
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = data.prediction || data.error;
    });
});
