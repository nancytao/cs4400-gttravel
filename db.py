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

# ismanager must be a 0 (false) or 1 (true)
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
        if e[1][-2:] == 'Y\'': # violates primary key constraint, username
            return 1
        elif e[1][-2:] == 'l\'': # violates email uniqueness constraint
            return 2
        else: # don't get here
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

        if result[0] == 1: # if Is_manager
            return 1
        else:
            return 2


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
