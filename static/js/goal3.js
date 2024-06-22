function predict() {
    var rainfall_monsoon = document.getElementById('rainfall_input').value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/goal3", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.retrievedData === 'No matching row found for the input value.') {
                    document.getElementById("retrievedData").innerHTML = "No matching row found for the input value.";
                    document.getElementById("prediction").innerHTML = "";
                    document.getElementById("predictionStatement").innerHTML = "";
                } else {
                    // Clear previous results
                    document.getElementById("retrievedData").innerHTML = "";
                    // Iterate over each record in retrievedData
                    response.retrievedData.forEach(function(record) {
                        // Display only the specified columns
                        var columnsToDisplay = ['Recharge from rainfall During Monsoon Season',
                                                'Recharge from rainfall During Non Monsoon Season',
                                                'Total Annual Ground Water Recharge',
                                                'Total Natural Discharges'];
                        columnsToDisplay.forEach(function(column) {
                            document.getElementById("retrievedData").innerHTML += column + ": " + record[column] + "<br>";
                        });
                    });
                    document.getElementById("prediction").innerHTML = "Prediction: " + response.prediction;
                    document.getElementById("predictionStatement").innerHTML = "Statement: " + response.statement;
                }
            } else {
                // Handle error case
                console.error("Error: " + xhr.status);
            }
        }
    };
    var data = JSON.stringify({rainfall_monsoon: rainfall_monsoon});
    xhr.send(data);
}
function logout() {
fetch('/go_home')
.then(response => {
if (response.redirected) {
    window.location.href = response.url; // Redirect to login page
}
})
.catch(error => console.error('Error:', error));
}