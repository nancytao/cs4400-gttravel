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


def register(username, email, password, ismanager):
    query = "INSERT INTO users(Username, Email, Password, Is_manager)"\
            "VALUES (%s, %s, %s, %s);"
    try:
        response = _cursor.execute(query, (username, email, password, ismanager))
    except Exception as e:
        print e[1]


# returns True if credentials are valid, else returns False
def login(username, password):
    query = "SELECT * FROM users WHERE Username = %s AND Password = %s;"
    response = _cursor.execute(query, (username, password))

    # clear cursor
    _cursor.fetchall()

    return response > 0


# returns True if user is a manager
def is_manager(username):
    query = "SELECT Is_manager FROM users WHERE Username = %s;"
    response = _cursor.execute(query, (username,))

    result = _cursor.fetchone()

    # sanity check
    _cursor.fetchall()

    return result[0] == 1


# main method for testing
setupConnection()

print "change this to test!!"

closeConnection()


# SQL Statements that may be required
# login
# 'SELECT * FROM USERS WHERE Username = %s AND Password = %s'
#
# register
# 'INSERT INTO users(Username, Email, Password, Is_manager) VALUES (%s, %s, %s, %s);'
#
# see past reviews
# 'SELECT * FROM city_reviews WHERE Username = %s'
# 'SELECT * FROM location_reviews WHERE Username = %s'
# 'SELECT * FROM event_reviews WHERE Username = %s'
#
# add city (as a manager)
# 'INSERT INTO city(City, Country, latitude, longitude, population) VALUES (%s, %s, %s, %s, %s)'
# for lang in languages_selected:
# 'INSERT INTO city_language(City, Country, Language) VALUES (%s, %s, lang)'
#
# city search
# query = ''
# if lang_selected:
#   for lang in
