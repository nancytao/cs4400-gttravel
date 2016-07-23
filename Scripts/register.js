/**
 * Created by coleb_000 on 7/13/2016.
 */
function toLogin() {
    var newUrl = "../templates/LoGiN.html";
    window.location.replace(newUrl);
}

function register() {
    var p1 = document.getElementById("p1").value;
    var p2 = document.getElementById("p2").value;
    var email = document.getElementById("email").value;
    var username = document.getElementById("username").value;

    if(false/*check nulls or empty strings etc*/) {
        document.getElementById("feedback").innerHTML = "One fo fields is left blank";
    } else if(p1 != p2) {
        document.getElementById("feedback").innerHTML = "Passwords dont match";
    } else if (p1.length < 6) {
        document.getElementById("feedback").innerHTML = "Password is too short";
    } else {
        //TODO SQL query
        window.location.replace("../templates/HomePage");
    }

}