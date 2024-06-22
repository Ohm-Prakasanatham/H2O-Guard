function getRecommendation() {
    var state = document.getElementById('state').value;
    var district = document.getElementById('district').value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/goal5", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var recommendation = JSON.parse(xhr.responseText);
            document.getElementById("recommendation").innerHTML = "<strong>Recommended Irrigation Type:</strong> " + recommendation['Irrigation Type'];
            document.getElementById("benefits").innerHTML = "<strong>Benefits:</strong> " + recommendation['Benefits'];
            document.getElementById("advantages").innerHTML = "<strong>Advantages:</strong> " + recommendation['Advantages'];
        }
    };
    xhr.send(JSON.stringify({state: state, district: district}));
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