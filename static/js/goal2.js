function predict() {
    var groundwater_recharge = document.getElementById('groundwater_input').value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/goal2", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (typeof response.TotalNaturalDischarges === 'undefined') {
                    document.getElementById("retrievedDataContent").innerHTML = "<a>Total Natural Discharges: No matching row found for the input value.</a><br>"
                                                                              + "<a>Annual Extractable Ground Water Resource: No matching row found for the input value.</a><br>"
                                                                              + "<a>Current Annual Ground Water Extraction For Irrigation: No matching row found for the input value.</a><br>"
                                                                              + "<a>Current Annual Ground Water Extraction For Domestic & Industrial Use: No matching row found for the input value.</a><br>";
                    document.getElementById("predictionValue").innerHTML = response['prediction'];
                    document.getElementById("overviewContent").innerHTML = response['overview'];
                } else {
                    document.getElementById("retrievedDataContent").innerHTML = "<a>Total Natural Discharges: " + response['TotalNaturalDischarges'] + "</a><br>"
                                                                              + "<a>Annual Extractable Ground Water Resource: " + response['Annual Extractable Ground Water Resource'] + "</a><br>"
                                                                              + "<a>Current Annual Ground Water Extraction For Irrigation: " + response['Current Annual Ground Water Extraction For Irrigation'] + "</a><br>"
                                                                              + "<a>Current Annual Ground Water Extraction For Domestic & Industrial Use: " + response['Current Annual Ground Water Extraction For Domestic & Industrial Use'] + "</a><br>";
                    document.getElementById("predictionValue").innerHTML = response['prediction'];
                    document.getElementById("overviewContent").innerHTML = response['overview'];
                }
                
            } else {
                // Handle error case
                console.error("Error: " + xhr.status);
            }
        }
    };
    var data = JSON.stringify({Annual_Ground_Water_Recharge: groundwater_recharge});
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