function startdone() {
    document.getElementById("startsc").hidden = true
    document.getElementById("loginscreen").hidden = false
}
function testRequestToLocalHost() {
    var request = new XMLHttpRequest();
    request.open('GET', 'http://localhost:3000/testreq');
    request.onload = function() {
        if (request.status === 200) {
            document.getElementById("startsc").hidden = true
            document.getElementById("loginscreen").hidden = false
        } else {
            document.getElementById("startsc").hidden = true
            document.getElementById("error").hidden = false
        }
    };
    request.onerror = function() {
        document.getElementById("startsc").hidden = true
        document.getElementById("error").hidden = false
    };
    request.send();
}