from flask import Flask, render_template, json, request, Response
import db

app = Flask(__name__)


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    """
    signs in user with given credentials
    Makes call to python wrapper
    logs user in or displays error message
    """

    # read the posted values from the UI
    if request.method == "POST":

        _name = request.form['usr']
        _password = request.form['pwd']
        num = db.login(_name,_password)

        if num == 1:
            # todo sql to get language/country
            countries = db.getCountries()
            languages = db.getLanguages()
            return render_template('managerpage.html', countries=countries, languages=languages)
        elif num == 2:
            return render_template('homepage.html')
        else:
            print "Credentials Incorrect"
            return


@app.route('/')
def main():
    """
    Starts app at login screen
    """
    db.setupConnection()
    return render_template('login.html')


@app.route("/testing")
def test():
    """
    Testing-can be deleted
    """
    return render_template('test.html')


@app.route("/to_register")
def to_register():
    """
    Takes user to register page
    """

    return render_template('register.html')


@app.route("/register")
def register():
    """
    Registers user then takes them to the home page
    """
    return render_template('homepage.html')


@app.route("/to_login")
def to_login():
    """
    Takes user to login page
    """
    return render_template("login.html")


@app.route("/login")
def login():
    """
    Login the user
    can replace or be replaced sign_up()
    """

    return render_template("homepage.html")


@app.route("/to_home")
def to_home():
    """
    Displays home page
    """

    return render_template('homepage.html')


@app.route("/to_country_search")
def to_country_search():
    """
    Takes users to country search page
    Dynamically auto fills forms from data base
    Test using Flask html template functionality
    """

    # return render_template('countrysearch.html')
    countries = db.getCountries()
    languages = db.getLanguages()
    """
    if request.form['submit'] == 'Select':
        resp = 'You chose: ', countries
        return Response(resp)
    """

    return render_template('countrysearchtemplate.html', option_list=countries, option_list2=languages)


@app.route("/to_city_search")
def to_city_search():
    """
    Takes users to city search page
    Dynamically auto fills forms from data base
    """
    # return render_template('countrysearch.html')
    countries = db.getCountries()
    cities = db.getCities()
    languages = db.getLanguages()
    """
    if request.form['submit'] == 'Select':
        resp = 'You chose: ', countries
        return Response(resp)
    """

    return render_template('citysearch.html', cities=cities, countries=countries, languages=languages)


@app.route("/to_location_search")
def to_location_search():
    """
    Takes users to location search page
    Dynamically auto fills forms from data base
    """
    # TODO get sql list of cities/location catagories
    cities = db.getCities()
    loc_cat = db.getLocTypes()
    """
     if request.form['submit'] == 'Select':
        resp = 'You chose: ', countries
        return Response(resp)
    """

    return render_template('locationsearch.html', cities=cities, loc_cat=loc_cat)


@app.route("/to_event_search")
def to_event_search():
    """
    Takes users to event search page
    Dynamically auto fills forms from data base
    """
    cities = db.getCities()
    event_cat = db.getEventCategories()
    """
    if request.form['submit'] == 'Select':
        resp = 'You chose: ', countries
        return Response(resp)
    """

    return render_template('eventsearch.html', cities=cities, event_cat=event_cat)


@app.route("/to_write_reviews")
def to_write_reviews():
    """
    Takes users to write reviews page
    """
    return render_template('writereviews.html')


@app.route("/to_past_reviews")
def to_past_reviews():
    """
    Takes users to past reviews page
    """
    return render_template('pastreviews.html')


@app.route("/to_country_results")
def search_country():
    """
    takes user to country results
    gets data from html form
    gets and loads table from database
    """
    return render_template('countryresults.html')


@app.route("/to_city_results")
def search_city():
    """
    takes user to city results
    gets data from html form
    gets and loads table from database
    """
    return render_template('cityresults.html')


@app.route("/to_event_results")
def search_events():
    """
    takes user to event results
    gets data from html form
    gets and loads table from database
    """
    return render_template('eventresults.html')


@app.route("/to_location_results")
def search_locations():
    """
    takes user to location results
    gets data from html form
    gets and loads table from database
    """
    return render_template('locationresults.html')


@app.route("/make_review")
def make_review():
    """
    takes user to past reveiws
    gets data from html form
    adds new review to database
    gets and loads table from database
    """
    return render_template('pastreviews.html')


if __name__ == '__main__':
    app.run()
