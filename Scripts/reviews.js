/**
 * Created by coleb_000 on 7/21/2016.
 */
function toHome() {
    var newUrl = "../templates/homepage.html";
    window.location.replace(newUrl);
}

function makeReview(){
    // not sure if right
    var subject = document.getElementById("subject").value;
    var date = document.getElementById("date").value;
    var score = document.getElementById("score").value;
    var description = document.getElementById("description").value;

    if(subject != null && date != null && score != null && description != null) {
        //add pop up the review has been made
        //TODO sql query with data above
    } else {
        document.getElementById("feedback").innerHTML = "One of the fields is empty";
        document.getElementById("feedback").setAttribute("Style","color: red");
    }



    window.location.replace("..templates/pastreviews.html")

}

