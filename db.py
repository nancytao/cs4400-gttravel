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

def test():
    _cursor.execute("INSERT INTO users(Username, Email, Password, Is_manager) VALUES"\
        "('name','filler@gmail.com','password',FALSE)")

    _cursor.execute("SELECT * FROM USERS")
    for row in _cursor.fetchall():
        print row[0]

    _database.commit()


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
