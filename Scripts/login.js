/**
 * Created by coleb_000 on 7/13/2016.
 */
function login () {

    var password = document.getElementById("pwd").value;
    var email = document.getElementById("usr").value;

    var newUrl = "../Layouts/Homepage.html";
    window.location.replace(newUrl);
    
}

function register() {
    var newUrl = "../Layouts/Register.html";
    window.location.replace(newUrl);
}

function forgot() {
    
}