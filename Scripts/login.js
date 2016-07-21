/**
 * Created by coleb_000 on 7/13/2016.
 */
function login () {

    var password = document.getElementById("pwd").value;
    var email = document.getElementById("usr").value;
    var storedPass = getPasswordFromDatabase(email);
    //TODO might default to empty string
    if(password === null || email === null) {
        document.getElementById("feedback").innerHTML = "One of the fields left blank";
    } else if(storedPass.isEqual(password)) { //TODO how to compare strings in javascript!
        var newUrl = "../templates/Homepage.html";
        window.location.replace(newUrl);
    } else {
        document.getElementById("feedback").innerHTML = "Passwords did not match";
    }


}

function getPasswordFromDatabase(email) {
    if(email === null) return null;
    var password = "1";
    //TODO sql to get pass based on email
    return password;
}

function register() {
    var newUrl = "../templates/Register.html";
    window.location.replace(newUrl);
}

function forgot() {

}