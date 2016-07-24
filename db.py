import config
import MySQLdb
import traceback


_connected = False
_database = None
_cursor = None

# setupConnection() must be called before anything else for this to work
# closeConnection() should be called after finishing


def setupConnection():
    global _connected
    global _database
    global _cursor

    if not _connected:
        try:
            _database = MySQLdb.connect(host="localhost",
                                        user="root",
                                        passwd=config.password,
                                        db="gttravel")
            _cursor = _database.cursor()
            _connected = True
        except Exception as e:
            _connected = False
            traceback.print_exc()


def closeConnection():
    global _connected

    if _connected:
        _database.close()
        _connected = False


# returns 1 if username is taken
# returns 2 if email is taken
# returns 0 if insert was valid
# returns 3 if everything is screwed
def register(username, email, password, ismanager):
    query = "INSERT INTO users(Username, Email, Password, Is_manager)"\
            "VALUES (%s, %s, %s, %s);"
    try:
        response = _cursor.execute(query, (username, email, password, ismanager))
        _database.commit()

        return 0
    except Exception as e:
        if e[1][-2:] == 'Y\'':  # violates primary key constraint, username
            return 1
        elif e[1][-2:] == 'l\'':  # violates email uniqueness constraint
            return 2
        else:  # don't get here
            return 3


# returns 0 if credentials are invalid
# returns 1 if user is a manager
# returns 2 if user is NOT a manager
def login(username, password):
    query = "SELECT * FROM users WHERE Username = %s AND Password = %s;"
    response = _cursor.execute(query, (username, password))

    # clear cursor
    _cursor.fetchall()

    if response == 0:
        return 0
    else:
        query = "SELECT Is_manager FROM users WHERE Username = %s;"
        response = _cursor.execute(query, (username,))

        result = _cursor.fetchone()

        # sanity check
        _cursor.fetchall()

        if result[0] == 1:  # if Is_manager
            return 1
        else:
            return 2


# does not error handle lmao
def addCity(city, country, latitude, longitude, population, languages):
    query = 'INSERT INTO city(City, Country, latitude, longitude, population) VALUES (%s, %s, %s, %s, %s)'
    response = _cursor.execute(query, (city, country, latitude, longitude, population))

    query = 'INSERT INTO city_language(City, Country, Language) VALUES (%s, %s, %s)'
    for lang in languages:
        response = _cursor.execute(query, (city, country, lang))

    _database.commit()


def getCountries():
    _cursor.execute("SELECT Country FROM country;")
    my_list = tupleListToList(_cursor.fetchall())
    my_list.append("")
    return my_list


def getLanguages():
    _cursor.execute("SELECT Language FROM language;")
    my_list = tupleListToList(_cursor.fetchall())
    my_list.append("Any additional language")
    return my_list


def getLanguagesMgr():
    _cursor.execute("SELECT Language FROM language;")
    return tupleListToList(_cursor.fetchall())


def getCities():
    _cursor.execute("SELECT City FROM city;")
    my_list = tupleListToList(_cursor.fetchall())
    my_list.append("")
    return my_list


def getLocTypes():
    _cursor.execute("SELECT Type FROM location_types;")
    return tupleListToList(_cursor.fetchall())


def getEventCategories():
    _cursor.execute("SELECT Category FROM event_categories;")
    return tupleListToList(_cursor.fetchall())


def tupleListToList(tuplelist):
    my_list = []
    for item in tuplelist:
        my_list.append(item[0])
    return my_list


# returns list in format [reviewed_item, review_date, score, text]
def pastReviews(username):
    reviews = []  # to return

    # city reviews!
    query = 'SELECT * FROM city_review WHERE Username = %s'
    response = _cursor.execute(query, (username,))
    for row in _cursor.fetchall():
        list1 = []
        list1.append(', '.join([row[1], row[2]]))
        for item in row[3:]:
            list1.append(item)
        reviews.append(list1)

    # location reviews
    query = 'SELECT * FROM location_review WHERE Username = %s'
    response = _cursor.execute(query, (username,))
    for row in _cursor.fetchall():
        list1 = []
        list1.append(', '.join([row[1], row[2], row[3]]))
        for item in row[4:]:
            list1.append(item)
        reviews.append(list1)

    # event reviews
    query = 'SELECT * FROM event_review WHERE Username = %s'
    response = _cursor.execute(query, (username,))
    for row in _cursor.fetchall():
        list1 = []
        list1.append(', '.join([row[1], str(row[2]), str(row[3]), row[4], row[5], row[6]]))
        for item in row[7:]:
            list1.append(item)
        reviews.append(list1)

    return reviews


def countrySearch(country, population_min, population_max, lang_list):
    population = population_max or population_min
    cri = False
    if "Any additional language" in lang_list:
        cri = True
        lang_list.remove('Any additional language')

    if country:
        query = "SELECT * FROM country WHERE Country = %s;"
        response = _cursor.execute(query, (country,))
        fetch = _cursor.fetchone()
        result = {}
        result['name'] = fetch[0]
        result['population'] = fetch[1]

        result['capitals'] = getCapitals(country)
        result['languages'] = getLanguagesCountry(country)

        return [result]
    elif population and lang_list:
        languages = '\' OR Language = \''.join(lang_list)
        langquery = 'Language = \'' + languages + '\''
        innerquery = "(SELECT * FROM country_language WHERE " + langquery + ") q "

        query = "SELECT * FROM " + innerquery + "NATURAL JOIN country) "
        if cri:
            query += "p "
            query = "SELECT * FROM multlangcountries NATURAL JOIN (" + query
        query += "WHERE "

        if population_min and population_max:
            query += "Population > %s AND Population < %s ORDER BY Population DESC"
            response = _cursor.execute(query, (population_min, population_max))
        elif population_max:
            query = query + "Population < %s ORDER BY Population DESC"
            print query
            response = _cursor.execute(query, (population_max,))
        elif population_min:
            query = query + "Population > %s ORDER BY Population DESC"
            response = _cursor.execute(query, (population_min,))
        else:
            print "shouldn't get here"  # sanity check

        result = []
        for item in _cursor.fetchall():
            put = {}
            put['name'] = item[0]
            put['population'] = item[1]
            put['capitals'] = getCapitals(item[0])
            put['languages'] = getLanguagesCountry(item[0])
            result.append(put)

        return result
    elif population:
        query = "SELECT Country, Population FROM country WHERE "

        response = ""

        if population_min != "" and population_max != "":
            query = query + "Population > %s AND Population < %s ORDER BY Population DESC;"
            response = _cursor.execute(query, (population_min, population_max))
        elif population_min == "" and population_max != "":
            query = query + "Population < %s ORDER BY Population DESC;"
            response = _cursor.execute(query, (population_max,))
        elif population_min != "" and population_max == "":
            query = query + "Population > %s ORDER BY Population DESC;"
            response = _cursor.execute(query, (population_min,))

        result = []
        for item in _cursor.fetchall():
            put = {}
            put['name'] = item[0]
            put['population'] = item[1]
            put['capitals'] = getCapitals(item[0])
            put['languages'] = getLanguagesCountry(item[0])
            result.append(put)

        return result
    elif lang_list:
        languages = '\' OR Language = \''.join(lang_list)
        langquery = 'Language = \'' + languages + '\''
        if cri:
            query = "SELECT * FROM multlangcountries NATURAL JOIN "\
            "(SELECT * FROM (SELECT Country FROM country_language WHERE "
            query += langquery + ") q NATURAL JOIN country) p;"
        else:
            query = "SELECT * FROM (SELECT Country FROM country_language WHERE "
            query += langquery + ") q NATURAL JOIN country;"
        response = _cursor.execute(query)

        result = []
        for item in _cursor.fetchall():
            put = {}
            put['name'] = item[0]
            put['population'] = item[1]
            put['capitals'] = getCapitals(item[0])
            put['languages'] = getLanguagesCountry(item[0])
            result.append(put)

        return result
    else:
        query = "SELECT * FROM country;"
        response = _cursor.execute(query)

        result = []
        for item in _cursor.fetchall():
            put = {}
            put['name'] = item[0]
            put['population'] = item[1]
            put['capitals'] = getCapitals(item[0])
            put['languages'] = getLanguagesCountry(item[0])
            result.append(put)

        return result


# returns a country's capitals in a string
def getCapitals(country):
    query = "SELECT Capital FROM capitals WHERE Country = %s;"
    response = _cursor.execute(query, (country,))
    capitals = []
    for row in _cursor.fetchall():
        capitals.append(row[0])
    capitals = ', '.join(capitals)
    return capitals


# returns a country's languages in a string
def getLanguagesCountry(country):
    query = "SELECT Language FROM country_language WHERE Country = %s;"
    response = _cursor.execute(query, (country,))
    languages = []
    for row in _cursor.fetchall():
        languages.append(row[0])
    languages = ', '.join(languages)
    return languages


# returns specific city in format [city, country, latitude, longitude,
#       population, is_capital, [languages]]
# returns
def citySearch(city, lang_list):
    if city:  # searching by city, returns just info about that city
        query = "SELECT * FROM city WHERE City = %s;"
        response = _cursor.execute(query, (city,))
        result = list(_cursor.fetchone())

        query = "SELECT * FROM capitals WHERE Capital = %s;"
        response = _cursor.execute(query, (city,))
        if response > 0:
            result.append(True)
        else:
            result.append(False)

        query = "SELECT Language FROM city_language WHERE City = %s;"
        response = _cursor.execute(query, (city,))

        languages = []
        for row in _cursor.fetchall():
            languages.append(row[0])

        result.append(languages)
        return result
    if lang_list != None:
        languages = '\' OR Language = \''.join(lang_list)
        langquery = 'Language = \'' + languages + '\''
        query = "SELECT * FROM city_language WHERE " + langquery
        response = _cursor.execute(query)

        for row in _cursor.fetchall():
            print row[0]


## testing
setupConnection()

# code for SELECT for testing :)
# _cursor.execute("SELECT * FROM city_language")
# for row in _cursor.fetchall():
#     print row

# citySearch(None, ['Spanish', 'French', 'Catalan'])
# print citySearch('Barcelona', None)
print countrySearch("", "", "", ['French', 'Any additional language'])

closeConnection()
