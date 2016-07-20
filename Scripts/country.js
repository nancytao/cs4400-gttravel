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
    //TODO use sql
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

/**
 * returns string array of Languages form sql query
 * @returns {string[]}
 */
function getLanguages() {
    //TODO use sql
    return ["a","b","c","d","e"];
}

/**
 * Auto populates checkboxes for languages
 */
function populateLanguages() {
    var list = getLanguages();

    for (var i = 0; i < list.length; i++) {
            /*
            <div class="checkbox">
            <label><input type="checkbox"> Dutch</label>
            </div>
            */
        //TODO Need to add IDs
        /*
        var div = document.createElement("div");
        div.class = "checkbox-inline";
        var label = document.createElement("label");
        var input = document.createElement("input");
        input.type = "checkbox";
        label.innerHTML = list[i];
        label.appendChild(input);
        div.appendChild(label);

        // add the label element to your div
        document.getElementById('languages').appendChild(div);
        */

        //TODO fix spacing try inner html from other code
        var checkbox = document.createElement('input');
        checkbox.type = "checkbox";
        checkbox.name = "name";
        checkbox.value = "value";
        checkbox.id = list[i];

        var label = document.createElement('label');
        label.htmlFor = list[i];
        label.appendChild(document.createTextNode(list[i]));

        var div = document.createElement("div");
        div.class = "checkbox-inline";
        div.appendChild(checkbox);
        div.appendChild(label);

        document.getElementById('languages').appendChild(div);



    }

}