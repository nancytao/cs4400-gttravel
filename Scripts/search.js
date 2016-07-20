/**
 * Created by coleb_000 on 7/20/2016.
 */
function toHome() {
    var newUrl = "../Layouts/HomePage.html";
    window.location.replace(newUrl);
}


/**
 * returns string array of country names from sql query
 * @returns {string[]}
 */
function getCountryNames() {
    //TODO use sql: SELECT Name FROM COUNTRY;
    return ["1","2","3","4","5"];
}

/**
 * Autopopulates the country name drop down menu
 */
function populateCountryNames() {

    var list = getCountryNames();

    var sel = document.getElementById('country');
    for(var i = 0; i < list.length; i++) {
        var opt = document.createElement('option');
        opt.innerHTML = list[i];
        opt.value = list[i];
        opt.id = list[i];
        sel.appendChild(opt);
    }

}

/**
* returns string array of country names form sql query
* @returns {string[]}
*/
function getCityNames() {
    //TODO use sql: SELECT City, Country FROM CITY;
    return ["1","2","3","4","5"];
}

/**
 * Takes in list of names and adds it to the drop down menu
 */
function populateCityNames() {

    var list = getCityNames();

    var sel = document.getElementById('city');
    for(var i = 0; i < list.length; i++) {
        var opt = document.createElement('option');
        opt.innerHTML = list[i];
        opt.value = list[i];
        opt.id = list[i];
        sel.appendChild(opt);
    }

}

/**
 * returns string array of Languages from sql query
 * @returns {string[]}
 */
function getLanguages() {
    //TODO use sql: SELECT Language FROM CITY_LANGUAGE;
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

/**
 * returns string array of event categories from sql query
 * @returns {string[]}
 */
function getEventCategories() {
    //TODO use sql: SELECT Category FROM EVENT_CATEGORIES;
    return ["a","b","c","d","e"];
}

/**
 * Auto populates checkboxes for event categories
 */
function populateEventCategories() {
    var list = getEventCategories();

    for (var i = 0; i < list.length; i++) {

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

        document.getElementById('categoriesE').appendChild(div);
    }

}

/**
 * returns string array of location types from sql query
 * @returns {string[]}
 */
function getLocationTypes() {
    //TODO use sql: SELECT Type FROM LOCATION_TYPES;
    return ["a","b","c","d","e"];
}

/**
 * Auto populates checkboxes for location types
 */
function populateLocationTypes() {
    var list = getLocationTypes();

    for (var i = 0; i < list.length; i++) {

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

        document.getElementById('categoriesL').appendChild(div);
    }

}