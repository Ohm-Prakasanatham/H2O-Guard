function predict() {
    var total_annual_ground_water_recharge = document.getElementById('total_annual_ground_water_recharge').value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/goal4", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            // Clear previous results
            document.getElementById("retrievedData").innerHTML = "";
            document.getElementById("prediction").innerHTML = "";
            document.getElementById("predictionStatement").innerHTML = "";

            if (response.retrievedData === 'No matching row found for the input value.') {
                // Handle case when no matching row is found
                document.getElementById("retrievedData").innerHTML = "No matching row found for the input value.";
                document.getElementById("prediction").innerHTML = "";
                document.getElementById("predictionStatement").innerHTML = "";
            } else {
                if ('retrievedData' in response) {
                    // Display retrieved data
                    var retrievedData = response.retrievedData[0];
                    var retrievedDataHtml = "<a>Total Annual Ground Water Recharge: " + retrievedData['Total Annual Ground Water Recharge'] + "</a><br>";
                    retrievedDataHtml += "<a>Annual Extractable Ground Water Resource: " + retrievedData['Annual Extractable Ground Water Resource'] + "</a><br>";
                    retrievedDataHtml += "<a>Current Annual Ground Water Extraction For Irrigation: " + retrievedData['Current Annual Ground Water Extraction For Irrigation'] + "</a><br>";
                    retrievedDataHtml += "<a>Current Annual Ground Water Extraction For Domestic & Industrial Use: " + retrievedData['Current Annual Ground Water Extraction For Domestic & Industrial Use'] + "</a><br>";
                    document.getElementById("retrievedData").innerHTML = retrievedDataHtml;
                }
                
                if ('prediction' in response) {
                    // Display prediction
                    document.getElementById("prediction").innerHTML = "<a>Prediction: " + response.prediction + "</a>";
                }

                if ('statement' in response) {
                    // Display prediction statement
                    document.getElementById("predictionStatement").innerHTML = "<a>Statement: " + response.statement + "</a>";
                }
            }
        }
    };
    var data = JSON.stringify({total_annual_ground_water_recharge: total_annual_ground_water_recharge});
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
