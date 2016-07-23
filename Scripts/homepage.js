/**
 * Created by coleb_000 on 7/13/2016.
 */

/**
 * Might not need this file
 */

function logout() {
    var newUrl = "../templates/login.html";
    window.location.replace(newUrl);
}

function databaseCoolness() {
    document.getElementById("test").innerHTML = "hi";
    $.ajax({
        url: "../test.py",
        type: 'POST',
        success: function(response){
            //here you do whatever you want with the response variable
            document.getElementById("test").innerHTML = response;
        }
    });
}