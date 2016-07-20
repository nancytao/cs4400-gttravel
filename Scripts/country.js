/**
 * Created by coleb_000 on 7/20/2016.
 */
function toHome() {
    var newUrl = "../Layouts/HomePage.html";
    window.location.replace(newUrl);
}


/**
 * returns string array of country names form sql query
 * @returns {string[]}
 */
function getNames() {

    return ["1","2","3","4","5"];
}

/**
 * Takes in list of names and adds it to the drop down menu
 */
function populateNames() {

    var list = getNames();

    var sel = document.getElementById('names');
    for(var i = 0; i < list.length; i++) {
        var opt = document.createElement('option');
        opt.innerHTML = list[i];
        opt.value = list[i];
        opt.id = list[i];
        sel.appendChild(opt);
    }

}