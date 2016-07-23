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


# returns False if credentials are invalid
# returns 1 if user is a manager
# returns 2 if user is NOT a manager
def login(username, password):
    query = "SELECT * FROM users WHERE Username = %s AND Password = %s;"
    response = _cursor.execute(query, (username, password))

    # clear cursor
    _cursor.fetchall()

    if response == 0:
        return False
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


# force adding languages for cities handled in GUI
# does not error handle lmao
def addCity(city, country, latitude, longitude, population, languages):
    query = 'INSERT INTO city(City, Country, latitude, longitude, population) VALUES (%s, %s, %s, %s, %s)'
    response = _cursor.execute(query, (city, country, latitude, longitude, population))

    query = 'INSERT INTO city_language(City, Country, Language) VALUES (%s, %s, %s)'
    for lang in languages:
        response = _cursor.execute(query, (city, country, lang))

    _database.commit()


def citySearch(city, lang_list):
    if city != None:
        query = "SELECT * FROM city WHERE City = %s;"
        response = _cursor.execute(query, (city,))
        result = list(_cursor.fetchone())

        query = "SELECT * FROM capitals WHERE Capital = %s;"
        response = _cursor.execute(query, (city,))
        if response > 0:
            result.append(True)
        else:
            result.append(False)

        query = "SELECT * FROM city_language WHERE City = %s;"
        response = _cursor.execute(query, (city,))

        languages = []
        for row in _cursor.fetchall():
            languages.append(row[2])

        result.append(languages)
        return result

    if lang_list != None:
        languages = '\' OR Language = \''.join(lang_list)
        langquery = 'Language = \'' + languages + '\''
        query = "SELECT * FROM city_language WHERE " + langquery
        response = _cursor.execute(query)
        for row in _cursor.fetchall():
            print row


def getCountries():
    _cursor.execute("SELECT Name FROM country;")
    return tupleListToList(_cursor.fetchall())


def getLanguages():
    _cursor.execute("SELECT Language FROM language;")
    return tupleListToList(_cursor.fetchall())


def tupleListToList(tuplelist):
    list = []
    for item in tuplelist:
        list.append(item[0])

    return list


setupConnection()

print "change this to test!!"

# code for SELECT for testing :)
# _cursor.execute("SELECT * FROM city_language")
# for row in _cursor.fetchall():
#     print row

closeConnection()


# SQL Statements that may be required
# see past reviews
# 'SELECT * FROM city_reviews WHERE Username = %s'
# 'SELECT * FROM location_reviews WHERE Username = %s'
# 'SELECT * FROM event_reviews WHERE Username = %s'
#
# city search
# query = ''
# if lang_selected:
#   for lang in
