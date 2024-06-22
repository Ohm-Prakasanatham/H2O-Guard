function redirect(url) {
    window.location.href = url;
}
function logout() {
fetch('/logout')
.then(response => {
    if (response.redirected) {
        window.location.href = response.url; // Redirect to login page
    }
})
.catch(error => console.error('Error:', error));
}