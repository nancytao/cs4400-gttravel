from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('login.html')


@app.route("/testing")
def test():
    return render_template('test.html')


@app.route("/to_register")
def to_register():
    return render_template('register.html')


@app.route("/register")
def register():
    return render_template('homepage.html')


@app.route("/to_login")
def to_login():
    return render_template('login.html')


@app.route("/login")
def login():
    return render_template('homepage.html')


@app.route("/to_home")
def to_home():
    return render_template('homepage.html')


@app.route("/to_country_search")
def to_country_search():
    return render_template('countrysearch.html')


@app.route("/to_city_search")
def to_city_search():
    return render_template('citysearch.html')


@app.route("/to_location_search")
def to_location_search():
    return render_template('locationsearch.html')


@app.route("/to_event_search")
def to_event_search():
    return render_template('eventsearch.html')


@app.route("/to_write_reviews")
def to_write_reviews():
    return render_template('writereviews.html')


@app.route("/to_past_reviews")
def to_past_reviews():
    return render_template('pastreviews.html')


@app.route("/to_country_results")
def search_country():
    return render_template('countryresults.html')


@app.route("/to_city_results")
def search_city():
    return render_template('cityresults.html')


@app.route("/to_event_results")
def search_events():
    return render_template('eventresults.html')


@app.route("/to_location_results")
def search_locations():
    return render_template('locationresults.html')

@app.route("/make_review")
def make_review():
    return render_template('pastreviews.html')


if __name__ == '__main__':
    app.run()
